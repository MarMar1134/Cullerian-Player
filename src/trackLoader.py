import jsonParser
import fileManager
import eyed3

# Prepares the logical object that's going to be used on the JSON parsing.
# Returns the track metadata.
def codifyTrack(pMonth:str, pPhraseDay:str):
    trackPath = fileManager.addTrack(pMonth[:3])

    if trackPath is None:
        print("No se pudo agregar la pista")
        return
    
    print(f"Pista agregada: {trackPath}")

    track = eyed3.load(trackPath)
    trackName = track.tag.title

    hasPhrase = pPhraseDay if not pPhraseDay == "" else ""

    print(trackName)

    trackMetadata = jsonParser.Encoder(
        pMonth=pMonth,
        pName=trackName,
        pAuthor=track.tag.artist,
        pTrackId=trackPath.stem,
        pPhraseDay=hasPhrase
    )

    return trackMetadata

# Copies the track from its source to the matching folder. Also codifies the metadata of the track and creates
# the phrase file if needed.
def insertTrack():
        trackMonth = input("Ingrese el mes donde ingresar la pista: ")

        hasPhrase = input("¿Tiene frase especial? (Y/N) ")

        if(hasPhrase.lower() == "y"):
            phraseDay = input("¿En que dia va? ")
            phrase = input("Ingrese la frase nueva: ")

            if(fileManager.addPhrase(trackMonth[:3], phraseDay, phrase)):
                codifiedTrack = codifyTrack(trackMonth, "")
            else:
                codifiedTrack = codifyTrack(trackMonth, phraseDay)

        codifiedTrack.encodeTrack()