import json
from pathlib import Path

baseDirectory = Path(__file__).resolve().parent
tracks = baseDirectory / "track_data" / "tracks.json"

def getTracksByMonth(month:str):
    with open(tracks) as f:
        tracksJson = json.load(f)
        
    return tracksJson[month]

def getTrackMetadata(month, trackId):
    return month[trackId]

def getTrackName(track):
    return track["name"]

def getTrackPath(track):
    return track["path"]

def getTrackAuthor(track):
    return track["author"]

class Encoder:
    def __init__(self ,pMonth:str, pName:str, pAuthor:str, pTrackId:str):
        self.month = pMonth.lower()
        self.trackId = pTrackId.lower().replace(" ","_")
        self.name = pName
        self.path = self.trackId + ".mp3"
        self.author = pAuthor

    def encodeTrack(self):
        if not tracks.exists():
            self._createEmptyTracksFile()

        try:
            with open(tracks, "r", encoding='utf-8') as file:
                existingTracks = json.load(file)
            
            if(self.month not in existingTracks):
                existingTracks[self.month] = {}

            trackData = {"name":self.name, "path":self.path,"author":self.author}
            existingTracks[self.month][self.trackId] = trackData

            with open(tracks, "w", encoding='utf-8') as file:
                json.dump(existingTracks, file, indent=3, ensure_ascii=False)
        
        except Exception as e:
            print(f"Ha ocurrido el siguiente error: {e}")