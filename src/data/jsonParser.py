"""An utility library used on JSON managment. Contains all the functions and methods used to read, iterate and
    write JSON files, mostly used for the tracks metadata. 
"""
import json
import random
from pathlib import Path

baseDirectory = Path(__file__).resolve().parent.parent.parent
tracksPath = baseDirectory / "assets" / "data" / "tracks.json"

def isJsonEmpty():
    return not tracksPath.exists()

# Returns the entire JSON ready to be read, without the necesity of re-open the actual file.
def getTracksJson():
    with open(tracksPath) as file:
        tracksJson = json.load(file)
        
    return tracksJson

# Returns the track's metadata. Is searched with the month and its own id.
def getTrackMetadata(pMonthId, pTrackId):
    tracksJson = getTracksJson()

    return tracksJson[pMonthId][pTrackId]

# Returns a random track from the current month.
def getRandomTrack(monthId: str):
    tracksJson = getTracksJson()

    trackIds = list(tracksJson[monthId].keys())
    randomTrackId = random.choice(trackIds)
    
    return tracksJson[monthId][randomTrackId]

# The only thing that justifies this being a class is comodity at the time of passing new data.
class Encoder:
    def __init__(self, pMonth:str, pName:str, pAuthor:str, pTrackId:str, pPhraseDay:str):
        self.month = pMonth[:3].lower()
        self.trackId = pTrackId.lower().replace(" ","_")
        self.name = pName
        self.path = self.month[:3] + "/" + self.trackId + ".mp3"
        self.author = pAuthor
        self.phrase = self.month[:3] + "_" + pPhraseDay + ".txt" if not pPhraseDay == "" else ""

    # Writes the data given on the constructor onto tracks.json
    def encodeTrack(self):
        try:
            tracksPath.parent.mkdir(parents=True, exist_ok=True)

            if (not tracksPath.exists()):
                with open(tracksPath, "w", encoding="utf-8") as file:
                    json.dump({}, file, indent=3, ensure_ascii=False)

            with open(tracksPath, "r", encoding='utf-8') as file:
                existingTracks = json.load(file)
            
            if(self.month not in existingTracks):
                existingTracks[self.month] = {}

            trackData = {"name":self.name, "path":self.path,"author":self.author, "phrase":self.phrase}

            existingTracks[self.month][self.trackId] = trackData

            with open(tracksPath, "w", encoding='utf-8') as file:
                json.dump(existingTracks, file, indent=3, ensure_ascii=False)
        
        except Exception as e:
            print(f"The following error just happened: {e}")
            print("We are on module jsonParser.py, encodeTrack()")