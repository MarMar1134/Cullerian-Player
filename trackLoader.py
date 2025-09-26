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
def trackPath(trackName):
    return baseDirectory / "audio_tracks" / (jsonParser.getTrackPath(trackName))

def getTrackData(trackName):
    return baseDirectory / "track_data" / (jsonParser.getTracksForMonth(trackName))

# Used to play tracks when is the correct date
def playTrack(trackPath):
    pygame.mixer.music.load(str(trackPath))
    pygame.mixer.music.play(loops=0)

    trackName = jsonParser.getTrackName(trackPath)
    trackAuthor = jsonParser.getTrackAuthor(trackPath)

    print(f"Reproduciendo: {trackName} - {trackAuthor}")

def randomTrack(trackList):
    return random.choice(trackList)

# Every track has its own path
julyNinthPath = trackPath("himno_nacional_argentino")
oktoberFirstPath = trackPath("fuegos_de_octubre")
novemberFirstPath = trackPath("dirge_for_november")
novemberFourthPath = trackPath("la_melodia_de_dios")
birthdayPath = trackPath("feliz_cum")
chrismasPath = trackPath("all_i_want_for_chrismas")

# Counter for stopping the track once finishes
trackCounter = 0

# A list of tracks
allTracks = [julyNinthPath, oktoberFirstPath, novemberFirstPath, novemberFourthPath, birthdayPath]
novemberTracks = [novemberFirstPath, novemberFourthPath]

# Infinite loop, it stops when the song finishes or if it isn´t an special day
while True:
    currentMonth = date.today().month
    currentDay = date.today().day
    try:
        # Depending on the month, diferent tracks will be played
        match currentMonth:
            case 7:
                print("Seamos libres, que lo demás no importa nada. Es 9 de julio")
                playTrack(julyNinthPath)
            case 10:
                print("Llegó la revolución, es 1 de octubre")
                playTrack(oktoberFirstPath)
            case 9:
                if (currentDay == 1):
                    print("Prepará el ataúd, es 1 de noviembre")
                    playTrack(novemberFirstPath)
                elif (currentDay == 4):
                    print("Hora de llorar, es 4 de noviembre")
                    playTrack(novemberFourthPath)
                else :
                    print("Reproduciendo una pista aleatoria de noviembre")
                    playTrack(randomTrack(novemberTracks))
            case 12:
                if (currentDay == 16):
                    print("Feliz cum, hijo de puta")
                    playTrack(birthdayPath)
                elif (currentDay == 25):
                    playTrack(chrismasPath)
            case _:
                print("Hoy no es un dia especial, acá tenés una pista aleatoria")
                randomChosenTrack = randomTrack(allTracks)
                playTrack(randomChosenTrack)

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