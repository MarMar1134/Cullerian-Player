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

    print(f"Reproduciendo: {trackName} - {trackAuthor}")

# Counter for stopping the track once finishes.
trackCounter = 0

# Infinite loop, it stops when the song finishes or by user's hand.
while True:
    currentMonth = date.today().month
    currentDay = date.today().day

    print("Bienvenido al reproductor Cullerio, ¿desea agregar una nueva canción? (Y/N)")
    answer = input()

    if(answer.lower() == "y"):
        trackLoader.insertTrack()
        break

    try:
        monthTracks = None
        currentTrack = None
        monthId = ""

        # A chech to see if this month exists.
        for month in Months:
            if currentMonth == month.value:
                monthId = month.name.lower()
                break

        trackId = fileManager.getDailyTrack(monthId, str(currentDay + 1))
            
        # If there's a track available for today, is set up to be played and is shown it's phrase.
        if(not trackId == ""):
            todaysPhrase = fileManager.getDailyPhrase(monthId, str(currentDay))
            print(todaysPhrase)

            currentTrack = newTrack(monthId, trackId)

        # If, somehow, the monthId wasn't set up, we break the loop and exit.
        if (monthId == ""):
            print("Al parecer, llegaste al mes 13...")
            break

        # If today there are no special tracks, we set up one randomly.
        if (currentTrack == None):
            print("No hay pistas especiales el dia de hoy, eligiendo pista aleatoria...")
            currentTrack = randomTrack(monthId)

        playTrack(currentTrack)
        trackCounter += 1

        # Prevents the script finishing before the song
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Once the song finishes, we ask the user if it wants to add a new track.
        if (trackCounter >= 1):
            print("Gracias por utilizar el reproductor Cullerio, ¿desea ingresar una nueva canción? (Y/N)")
            answer = input()
            
            if (answer.lower() == "y"):
                trackLoader.insertTrack()
            else:
                print("Entendido, ¡adios!")
                break

    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
        break