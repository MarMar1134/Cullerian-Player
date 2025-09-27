def getTrackAttributes():
    trackMonth = input("ingrese el mes donde incluir la pista: ")
    trackName = input("Ingrese el nombre de la pista: ")
    trackAuthor = input("Ingrese el o los autores, separados con coma: ")

    return trackMonth, trackName, trackAuthor

def postTrack(answer:str):
    import jsonParser
    match answer.lower():
        case "n":
            print("Entendido, ¡adios!")
        case "y":
            trackMonth, trackName, trackAuthor = getTrackAttributes()
        case _:
            print("Respuesta incorrecta. Cerrando programa...", answer)

    if(not trackMonth == "" or not trackName == "" or not trackAuthor == ""):
        newTrack = jsonParser.Encoder(
            pMonth=trackMonth,
            pName=trackName,
            pAuthor=trackAuthor,
            pTrackId= trackName.lower().replace(" ","_")
        )

        newTrack.encodeTrack()