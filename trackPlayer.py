import pygame
import jsonParser
import trackLoader
from datetime import date
from pathlib import Path

# Start of pygame
pygame.mixer.init()

# We the root directory
baseDirectory = Path(__file__).resolve().parent

# Returns all the tracks of a month
def getTracksByMonth(monthId:str):
    return jsonParser.getTracksByMonth(monthId)

# Returns the metadata of the selected track
def newTrack(month, trackId:str):
    return jsonParser.getTrackMetadata(month, trackId)

# Selects a random track from the passed month
def randomTrack(monthId:str):
    return jsonParser.getRandomTrack(monthId)

# Used to play tracks when is the correct date
def playTrack(trackMetadata):
    trackName = jsonParser.getTrackName(trackMetadata)
    trackPath = baseDirectory / "assets/audio" / (trackMetadata["path"])
    trackAuthor = jsonParser.getTrackAuthor(trackMetadata)

    pygame.mixer.music.load(str(trackPath))
    pygame.mixer.music.play(loops=0)

    print(f"Reproduciendo: {trackName} - {trackAuthor}")

# Counter for stopping the track once finishes
trackCounter = 0

# Infinite loop, it stops when the song finishes or if it isn´t an special day
while True:
    currentMonth = date.today().month
    currentDay = date.today().day

    print("Bienvenido al reproductor Cullerio, ¿desea agregar una nueva canción? (Y/N)")
    answer = input()

    if(answer.lower() == "y"):
        trackLoader.postTrack(answer)
        break

    try:
        monthTracks = None
        currentTrack = None
        monthId = ""

        # Depending on the month, diferent tracks will be played
        try:
            match currentMonth:
                case 1:
                    monthId = "january"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay==20):
                        print("A cortar orejas, es 20 de enero")
                        currentTrack = newTrack(monthTracks, "20_de_enero")
                    elif(currentDay==26):
                        print("Bienvenido al mundo, Wolfgang. Es 26 de enero")
                        currentTrack = newTrack(monthTracks, "")
                case 2:
                    monthId = "febreuary"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay==6):
                        print("Que se haga el amor, es 6 de febrero")
                        currentTrack = newTrack(monthTracks, "is_this_love")
                case 3:
                    monthId = "march"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay==26):
                        print("Descansá en paz, Ludwig. Es 26 de marzo")
                        currentTrack = newTrack(monthTracks, "5_sinfonia-movimiento_1")
                case 4:
                    monthId = "april"
                    monthTracks =getTracksByMonth(monthId)

                    if(currentDay==20):
                        print("El mundo arderá, es 20 de abril")
                        currentTrack = newTrack(monthTracks,"erika")
                case 5:
                    monthId = "may"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay==5):
                        print("Unidos venceremos, es 5 de mayo")
                        currentTrack = newTrack(monthTracks, "marcha_sovietica")
                    if(currentDay==25):
                        print("¡Viva la Patria! Es 25 de mayo")
                        currentTrack = newTrack(monthTracks, "marcha_de_san_lorenzo")
                case 6:
                    monthId = "june"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay==18):
                        print("Hora de la liberación, es 18 de junio")
                        currentTrack = newTrack(monthTracks, "hope_of_deliverance")
                    elif(currentDay==21):
                        print("El invierno ha llegado, es 21 de junio")
                        currentTrack = newTrack(monthTracks, "the_leper_affinity")
                case 7:
                    monthId = "july"
                    monthTracks = getTracksByMonth(monthId)
                    
                    if (currentDay == 9):
                        print("Seamos libres, que lo demás no importa nada. Es 9 de julio")
                        currentTrack = newTrack(monthTracks, "himno_nacional_argentino")
                case 8:
                    monthId = "august"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay==29):
                        print("El rey ha llegado, es 29 de agosto")
                        currentTrack = newTrack(monthTracks, "beat_it")
                case 9:
                    monthId = "september"
                    monthTracks = getTracksByMonth(monthId)

                    if(currentDay == 30):
                        print("El final se acerca, es 30 de septiembre")
                        currentTrack = newTrack(monthTracks, "wake_me_up_when_september_ends")
                case 10:
                    monthId = "october"
                    monthTracks = getTracksByMonth(monthId)
                    
                    if(currentDay == 1):
                        print("Llegó la revolución, es 1 de octubre")
                        currentTrack = newTrack(monthTracks, "fuegos_de_octubre")
                    elif(currentDay==17):
                        print("Un movimiento popular acecha, es 17 de octubre")
                        currentTrack = newTrack(monthTracks, "marcha_peronista")
                    elif(currentDay==25):
                        print("El Zar ha caido, es 25 de octubre")
                        currentTrack = newTrack(monthTracks, "rasputin")
                case 11:
                    monthId = "november"
                    monthTracks = getTracksByMonth(monthId)

                    if (currentDay == 4):
                        print("Hora de llorar, es 4 de noviembre")
                        currentTrack = newTrack(monthTracks, "la_melodia_de_dios")
                case 12:
                    monthId = "december"
                    monthTracks = jsonParser.getTracksByMonth(monthId)

                    if (currentDay == 16):
                        print("Feliz cum, hijo de puta")
                        currentTrack = newTrack(monthTracks, "feliz_cum")
                    elif (currentDay == 25):
                        currentTrack = newTrack(monthTracks, "all_i_want_for_chrismas")
                case _:
                    print("¿Que hiciste para llegar acá?")
                    break

        except Exception as e:
            print(f"Ha ocurrido el siguiente error: {e}")

        if (currentTrack == None):
            print("No hay pistas especiales el dia de hoy, eligiendo pista aleatoria...")
            currentTrack = randomTrack(monthId)

        playTrack(currentTrack)
        trackCounter += 1

        # Prevents the script finishing before the song
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        if (trackCounter >= 1):
            print("Gracias por utilizar el reproductor Cullerio, ¿desea ingresar una nueva canción? (Y/N)")
            answer = input()
            
            trackLoader.postTrack(answer)

    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
        break