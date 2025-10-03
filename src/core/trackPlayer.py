import pygame
from data import jsonParser, fileManager
from datetime import date
from pathlib import Path
from enum import Enum

# For comodity, the months are a pair (<MONTH_NAME>, <MONTH_CARDINAL>).
class Months(Enum):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12

# Start of pygame.
pygame.mixer.init()

# This allows the program to work on any machine.
currentFile = Path(__file__).resolve()
srcDirectory = currentFile.parent.parent
root = srcDirectory.parent

baseDirectory = root

# Returns the track's metadata.
def newTrack(pMonthId:str, trackId:str):
    return jsonParser.getTrackMetadata(pMonthId, trackId)

# Returns a random track from the current month.
def randomTrack(monthId:str):
    return jsonParser.getRandomTrack(monthId)

# Plays the selected track once. Also displays some of its metadata.
def getTrackData(trackMetadata):
    trackName = trackMetadata["name"]
    trackPath = baseDirectory / "assets/audio" / (trackMetadata["path"])
    trackAuthor = trackMetadata["author"]

    return trackName, trackAuthor, trackPath

def noTracksLoaded():
    return jsonParser.isJsonEmpty()

def getDailyTrack():
    currentMonth = date.today().month
    currentDay = date.today().day

    currentTrack = None
    monthId = ""
    todaysPhrase = ""

    # A chech to see if this month exists.
    for month in Months:
        if currentMonth == month.value:
            monthId = month.name.lower()
            break

    trackId = fileManager.getDailyTrack(monthId, str(currentDay))
            
    # If there's a track available for today, is set up to be played and is shown it's phrase.
    if(not trackId == ""):
        todaysPhrase = fileManager.getDailyPhrase(monthId, str(currentDay))

        currentTrack = newTrack(monthId, trackId)

    try:
        # If today there are no special tracks, we set up one randomly.
        if (currentTrack == None):
            currentTrack = randomTrack(monthId)
    except Exception as e:
        return None, e

    return currentTrack, todaysPhrase