from pathlib import Path

baseDirectory = Path(__file__).resolve().parent.parent.parent
audioDirectory = baseDirectory / "assets" / "audio"
phrasesDirectory = baseDirectory / "assets" / "phrases"

# Defines a directory for the phrase file. If the phrase doesn't exist, it put him on the directory.
# Returns True if the phrase didn't exist, False otherwise.
def addPhrase(pMonthId:str, pDay:str, pPhrase:str):
    if (not phrasesDirectory.exists()):
        phrasesDirectory.mkdir(parents=True, exist_ok=True)

    monthPath = phrasesDirectory / pMonthId
    phrasePath = monthPath / (pMonthId + "_" + pDay + ".txt")

    if(not monthPath.exists()):
       monthPath.mkdir(parents=True, exist_ok=True)

    if(phrasePath.exists()):
        print("This day already has a phrase.")
        return False

    try:
        with open(phrasePath, "w", encoding="utf-8") as file:
            file.write(pPhrase)

    except Exception as e:
        print(f"The following error just happened: {e}")
        print("We are on module fileManager.py, addPhrase()")

# With the passed month and day, determines with phrase is the one that goes.
# Returns the phrase i found, an empty string otherwise.
def getDailyPhrase(pMonth:str, pDay:str):
    monthPath = phrasesDirectory / pMonth[:3]
    phraseFile = pMonth + "_" + pDay + ".txt"
    phrasePath = monthPath / phraseFile

    if(not phrasePath.exists()):
        print("This day has no special phrase.\n")
        return ""
    
    try:
        with open(phrasePath, "r", encoding="utf-8") as file:
            currentPhrase = file.read()
        
        return currentPhrase
    except Exception as e:
        print(f"The following error just happened: {e}")
        print("We are on module fileManager.py, getDailyPhrase()")

# Copies the track from its source to his directory, based on the month selected by the user.
# Returns the new location of the track.
def addTrack(pMonthId:str, pTrackPath:Path):
    from customtkinter  import filedialog

    """track = filedialog.askopenfilename(
        title="Track selector",
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg")]
    )

    if (not track):
        print("No files found")
        return None

    trackPath = Path(track)

    if (not trackPath.exists()):
        trackPath.mkdir(parents=True, exist_ok=True)"""

    try:
        with open(pTrackPath, "rb") as file:
            fileData = file.read()

        monthPath = audioDirectory / pMonthId

        if(not monthPath.exists()):
            Path(monthPath).mkdir(parents=True, exist_ok=True)

        newPath = monthPath / pTrackPath.name

        with open(newPath, "wb") as copy:
            copy.write(fileData)

    except Exception as e:
        print(f"The following error just happened: {e}")
        print("We are on module fileManager.py, addTrack()")
        return None

    return newPath

def getBaseTrackPath():
    from customtkinter import filedialog

    track = filedialog.askopenfilename(
        title="Track selector",
        filetypes=[("Audio files", "*.mp3 *.wav *.ogg")]
    )

    if (not track):
        return None
    
    trackPath = Path(track)

    return trackPath

# With the current month and day, determines wich track needs to be played. Returns its id if found, an empty
# string otherwise.
def getDailyTrack(pMonthId:str, pDay:str):
    from data import jsonParser

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

if __name__ == "__main__":
    print(baseDirectory)