import pygame
import random
import jsonParser
from datetime import date
from pathlib import Path

# Start of pygame
pygame.mixer.init()

# We the root directory
baseDirectory = Path(__file__).resolve().parent

# Used to define tracks directory
def getTrackPath(trackName):
    return baseDirectory / "audio_tracks" / (jsonParser.getTrackPath(trackName))

# Used to play tracks when is the correct date
def playTrack(trackMetadata):
    trackName = jsonParser.getTrackName(trackMetadata)
    trackPath = baseDirectory / "audio_tracks" / (trackMetadata["path"])
    trackAuthor = jsonParser.getTrackAuthor(trackMetadata)

    pygame.mixer.music.load(str(trackPath))
    pygame.mixer.music.play(loops=0)

    print(f"Reproduciendo: {trackName} - {trackAuthor}")

def randomTrack(trackList):
    return random.choice(trackList)

def newTrack(month, trackId):
    return jsonParser.getTrackMetadata(month, trackId)

def getMonthlyTracks(monthId:str):
    return jsonParser.getTracksByMonth(monthId)

# Counter for stopping the track once finishes
trackCounter = 0

# Infinite loop, it stops when the song finishes or if it isn´t an special day
while True:
    currentMonth = date.today().month
    currentDay = date.today().day
    try:
        monthTracks = None
        currentTrack = None
        # Depending on the month, diferent tracks will be played
        match currentMonth:
            case 7:
                monthTracks = getMonthlyTracks("july")
                print("Seamos libres, que lo demás no importa nada. Es 9 de julio")
                
                currentTrack = newTrack(monthTracks, "himno_nacional_argentino")
            case 10:
                monthTracks = getMonthlyTracks("october")
                
                print("Llegó la revolución, es 1 de octubre")
                currentTrack = newTrack(monthTracks, "fuegos_de_octubre")
            case 11:
                monthTracks = getMonthlyTracks("november")

                if (currentDay == 1):
                    print("Prepará el ataúd, es 1 de noviembre")
                    currentTrack = newTrack(monthTracks, "dirge_for_november")
                elif (currentDay == 4):
                    print("Hora de llorar, es 4 de noviembre")
                    currentTrack = newTrack(monthTracks, "la_melodia_de_dios")
                else :
                    currentTrack = newTrack(monthTracks, "dirge_for_november")
                    
                    print("default hacia",jsonParser.getTrackName(currentTrack))
            case 12:
                monthTracks = jsonParser.getTracksByMonth("december")

                if (currentDay == 16):
                    print("Feliz cum, hijo de puta")
                    currentTrack = newTrack(monthTracks, "feliz_cum")
                elif (currentDay == 25):
                    currentTrack = newTrack(monthTracks, "all_i_want_for_chrismas")
            case _:
                print("¿Que hiciste para llegar acá?")
                break
            
        if (currentTrack == None):
            print("No hay pistas el dia de hoy")
            break

        playTrack(currentTrack)
        trackCounter += 1

        # Prevents the script finishing before the song
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        if (trackCounter >= 1):
            print("Que tenga un gran dia")
            break

    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
        break