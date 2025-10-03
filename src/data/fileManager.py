"""Utility library for file management. Used to check, copy and generate .txt, .mp3 and .json files, with
its respective paths if needed."""

from pathlib import Path
from src.log import logConfig

baseDirectory = Path(__file__).resolve().parent.parent.parent
audioDirectory = baseDirectory / "assets" / "audio"
phrasesDirectory = baseDirectory / "assets" / "phrases"

def addPhrase(pMonthId:str, pDay:str, pPhrase:str):
    """Defines a directory for the phrase file. If the phrase doesn't exist, it put him on the directory.
    Returns True if the phrase didn't exist, False otherwise."""

    if (not phrasesDirectory.exists()):
        phrasesDirectory.mkdir(parents=True, exist_ok=True)

    monthPath = phrasesDirectory / pMonthId
    phrasePath = monthPath / (pMonthId + "_" + pDay + ".txt")

    if(not monthPath.exists()):
       monthPath.mkdir(parents=True, exist_ok=True)

    if(phrasePath.exists()):
        logConfig.logger.warning(f"This day already has a phrase: {pMonthId}_{pDay}")
        return False

    try:
        with open(phrasePath, "w", encoding="utf-8") as file:
            file.write(pPhrase)

            logConfig.logger.info(f"A new phrase has been added: {phrasePath}")

    except Exception as e:
        logConfig.logger.error(f"An error happende while trying to add the Phrase: {e}", exc_info=True)

def getDailyPhrase(pMonth:str, pDay:str):
    """With the passed month and day, determines with phrase is the one that goes.
    Returns the phrase found, an empty string otherwise."""

    monthPath = phrasesDirectory / pMonth[:3]
    phraseFile = pMonth + "_" + pDay + ".txt"
    phrasePath = monthPath / phraseFile

    if(not phrasePath.exists()):
        logConfig.logger.info(f"This day has no special phrase: {pMonth}_{pDay}")
        return ""
    
    try:
        with open(phrasePath, "r", encoding="utf-8") as file:
            currentPhrase = file.read()
        
        return currentPhrase
    except Exception as e:
        logConfig.logger.error(f"An error happended while trying to get the daily phrase: {e}", exc_info=True)
        return ""

# Copies the track from its source to his directory, based on the month selected by the user.
# Returns the new location of the track.
def addTrack(pMonthId:str, pTrackPath:Path):
    """Copies the track from its source to his directory, based on the month selected by the user.
    Returns the new location of the track."""

    try:
        with open(pTrackPath, "rb") as file:
            fileData = file.read()

        monthPath = audioDirectory / pMonthId

        if(not monthPath.exists()):
            Path(monthPath).mkdir(parents=True, exist_ok=True)

        newPath = monthPath / pTrackPath.name

        with open(newPath, "wb") as copy:
            copy.write(fileData)

        logConfig.logger.info(f"A new track has been added: {newPath}")

    except Exception as e:
        logConfig.logger.error(f"An error happende while trying to add the track: {e}", exc_info=True)
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

def getDailyTrack(pMonthId:str, pDay:str):
    """
        Returns the track ID for the specified month and day if a special track is assigned; otherwise, returns an empty string.
    """

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