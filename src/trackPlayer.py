import pygame
import jsonParser
import trackLoader
import fileManager
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
baseDirectory = Path(__file__).resolve().parent

# Returns the track's metadata.
def newTrack(pMonthId:str, trackId:str):
    return jsonParser.getTrackMetadata(pMonthId, trackId)

# Returns a random track from the current month.
def randomTrack(monthId:str):
    return jsonParser.getRandomTrack(monthId)

# Plays the selected track once. Also displays some of its metadata.
def playTrack(trackMetadata):
    trackName = trackMetadata["name"]
    trackPath = (baseDirectory.parent) / "assets/audio" / (trackMetadata["path"])
    trackAuthor = trackMetadata["author"]

    pygame.mixer.music.load(str(trackPath))
    pygame.mixer.music.play(loops=0)

    print(f"Playing: {trackName} - {trackAuthor}")

# Counter for stopping the track once finishes.
trackCounter = 0

# Infinite loop, it stops when the song finishes or by user's hand.
while True:
    currentMonth = date.today().month
    currentDay = date.today().day

    try:
        monthTracks = None
        currentTrack = None
        monthId = ""

        # A chech to see if this month exists.
        for month in Months:
            if currentMonth == month.value:
                monthId = month.name.lower()
                break

        if (jsonParser.isJsonEmpty()):
            answer = input("Welcome to the Cullerian Player! To start, you need to add a track: (Y/N)")
            
            if(answer.lower() == "y"):
                trackLoader.insertTrack()
                break
            else:
                print("All right, good bye then!")
                break

        trackId = fileManager.getDailyTrack(monthId, str(currentDay))
         
        # If there's a track available for today, is set up to be played and is shown it's phrase.
        if(not trackId == ""):
            todaysPhrase = fileManager.getDailyPhrase(monthId, str(currentDay))
            print(todaysPhrase)

            currentTrack = newTrack(monthId, trackId)

        # If, somehow, the monthId wasn't set up, we break the loop and exit.
        if (monthId == ""):
            print("Somehow, you discovered month 13...")
            break

        try:
            # If today there are no special tracks, we set up one randomly.
            if (currentTrack == None):
                print("There are now special tracks today. Choosing a random one...")
                currentTrack = randomTrack(monthId)
        except Exception as e:
            answer = input(f"It seems that there are no tracks for your month, ¿do you want to add one?")
            
            if(answer.lower() == "y"):
                trackLoader.insertTrack()
                break
            else:
                print("All right, good bye then!")
                break

        playTrack(currentTrack)
        trackCounter += 1

        # Prevents the script finishing before the song
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Once the song finishes, we ask the user if it wants to add a new track.
        if (trackCounter >= 1):
            print("Thanks for utilize the Cullerian Player!, do you want to add another track? (Y/N)")
            answer = input()
            
            if (answer.lower() == "y"):
                trackLoader.insertTrack()
            else:
                print("Undestood, good bye!")
                break

    except KeyboardInterrupt:
        print("Track stopped by user input.\n")
        pygame.mixer.music.stop()

        print("Thanks for utilize the Cullerian Player!, do you want to add another track? (Y/N)")
        answer = input()
            
        if (answer.lower() == "y"):
            trackLoader.insertTrack()
        else:
            print("Undestood, good bye!")
            break
        break