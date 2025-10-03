import eyed3
from data import jsonParser, fileManager

# Prepares the logical object that's going to be used on the JSON parsing.
# Returns the track metadata.
def codifyTrack(pMonth:str, pPhraseDay:str):
    trackPath = fileManager.addTrack(pMonth[:3])

    if trackPath is None:
        print("The track couldn't be added.")
        return
    
    print(f"Track added succesfully to the following path: {trackPath}")

    track = eyed3.load(trackPath)
    trackName = track.tag.title

    phraseDay = pPhraseDay if not pPhraseDay == "" else ""

    trackMetadata = jsonParser.Encoder(
        pMonth=pMonth,
        pName=trackName,
        pAuthor=track.tag.artist,
        pTrackId=trackPath.stem,
        pPhraseDay=phraseDay
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

        else:
             codifiedTrack = codifyTrack(trackMonth, "")

        if codifiedTrack is None:
             print("Error, track couldn't be loaded.")
             return
        else:
             codifiedTrack.encodeTrack()

if __name__ == "__main__":
     insertTrack()