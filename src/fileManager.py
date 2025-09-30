from tkinter import Tk, filedialog
from pathlib import Path

baseDirectory = Path(__file__).resolve().parent
audioDirectory = (baseDirectory.parent) / "assets" / "audio"
phrasesDirectory = (baseDirectory.parent) / "assets" / "phrases"

def addPhrase(pMonthId:str, pDay:str, pPhrase:str):
    monthPath = phrasesDirectory / pMonthId
    phrasePath = monthPath / (pMonthId + "_" + pDay + ".txt")

    if(not monthPath.exists()):
        Path(monthPath).mkdir()

    if(phrasePath.exists()):
        print("El dia solicitado ya existe")
        return False

    try:
        with open(phrasePath, "w", encoding="utf-8") as file:
            file.write(pPhrase)

    except Exception as e:
        print(f"Ha ocurrido el siguiente error: {e}")

def getDailyPhrase(pMonth:str, pDay:str):
    monthPath = phrasesDirectory / pMonth[:3]
    phraseFile = pMonth + "_" + pDay + ".txt"
    phrasePath = monthPath / phraseFile

    if(not phrasePath.exists()):
        print("El dia solicitado no tiene una frase especial\n")
        print(phrasePath)
        return ""
    
    try:
        with open(phrasePath, "r", encoding="utf-8") as file:
            currentPhrase = file.read()
        
        return currentPhrase
    except Exception as e:
        print(f"Ha ocurrido el siguiente error: {e}")

def addTrack(pMonthId:str):
    root = Tk()
    root.withdraw()

    track = filedialog.askopenfilename(
        title="Selecciona una pista",
        filetypes=[("Archivos de audio", "*.mp3 *.wav *.ogg")]
    )

    if not track:
        print("No se seleccionó ningún archivo")
        return None

    trackPath = Path(track)

    try:
        with open(trackPath, "rb") as file:
            fileData = file.read()

        monthPath = audioDirectory / pMonthId

        if(not monthPath.exists()):
            Path(monthPath).mkdir()

        newPath = monthPath / trackPath.name

        with open(newPath, "wb") as copy:
            copy.write(fileData)

    except Exception as e:
        print(f"Ha ocurrido el siguiente error: {e}")
        root.destroy()
        return None

    root.destroy()
    return newPath

def getDailyTrack(pMonthId:str, pDay:str):
    import jsonParser

    tracksJson = jsonParser.getTracksJson()

    phraseFile = pMonthId[:3] + "_" + pDay

    phraseFound = False
    
    for month, tracks in tracksJson.items():
        for trackId, trackMetadata in tracks.items():
            currentPhrase = Path(trackMetadata["phrase"])
            
            if phraseFile ==  currentPhrase.stem:
                phraseFound = True
                return trackId

        if phraseFound:
            break

    return ""