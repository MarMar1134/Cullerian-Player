"""An utility library used on JSON managment. Contains all the functions and methods used to read, iterate and
    write JSON files, mostly used for the tracks metadata. 
"""
import json
import random
from pathlib import Path

baseDirectory = Path(__file__).resolve().parent
tracks = (baseDirectory.parent) / "assets/data" / "tracks.json"

def getTracksJson():
    with open(tracks) as file:
        tracksJson = json.load(file)
        
    return tracksJson

def getTrackMetadata(pMonthId, pTrackId):
    with open(tracks) as file:
        tracksJson = json.load(file)

    return tracksJson[pMonthId][pTrackId]

def getRandomTrack(monthId: str):
    with open(tracks) as file:
        tracksJson = json.load(file)

    trackIds = list(tracksJson[monthId].keys())
    randomTrackId = random.choice(trackIds)
    
    return tracksJson[monthId][randomTrackId]


class Encoder:
    def __init__(self, pMonth:str, pName:str, pAuthor:str, pTrackId:str, pPhraseDay:str):
        self.month = pMonth[:3].lower()
        self.trackId = pTrackId.lower().replace(" ","_")
        self.name = pName
        self.path = self.month[:3] + "/" + self.trackId + ".mp3"
        self.author = pAuthor
        self.phrase = self.month[:3] + "_" + pPhraseDay + ".txt" if not pPhraseDay == "" else ""

    def encodeTrack(self):
        if not tracks.exists():
            self._createEmptyTracksFile()

        try:
            with open(tracks, "r", encoding='utf-8') as file:
                existingTracks = json.load(file)
            
            if(self.month not in existingTracks):
                existingTracks[self.month] = {}

            trackData = {"name":self.name, "path":self.path,"author":self.author, "phrase":self.phrase}

            existingTracks[self.month][self.trackId] = trackData

            with open(tracks, "w", encoding='utf-8') as file:
                json.dump(existingTracks, file, indent=3, ensure_ascii=False)
        
        except Exception as e:
            print(f"Ha ocurrido el siguiente error: {e}")