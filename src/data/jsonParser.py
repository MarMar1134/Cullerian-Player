"""An utility library used on JSON managment. Contains all the functions and methods used to read, iterate and
    write JSON files, mostly used for the tracks metadata. 
"""
import json
import random
from pathlib import Path
from src.log import logConfig

baseDirectory = Path(__file__).resolve().parent.parent.parent
tracksPath = baseDirectory / "assets" / "data" / "tracks.json"

def isJsonEmpty():
    return not tracksPath.exists()

def getTracksJson():
    """Returns the entire JSON ready to be read, without the necesity of re-open the actual file."""

    with open(tracksPath) as file:
        tracksJson = json.load(file)
        
    return tracksJson

def getTrackMetadata(pMonthId, pTrackId):
    """Returns the track's metadata. Is searched with the month and its own id."""

    tracksJson = getTracksJson()

    return tracksJson[pMonthId][pTrackId]

def getRandomTrack(monthId: str):
    """Returns a random track's metadata from the current month."""
    tracksJson = getTracksJson()

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
        self.phrase = self.month[:3] + "_" + pPhraseDay + ".txt" if not pPhraseDay is None else ""

    def encodeTrackData(self):
        """Writes the data given on the constructor onto tracks.json"""

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

            logConfig.logger.info(f"Track data added-id:{self.trackId}, path:{self.path}")
            
            return True
        except Exception as e:
            logConfig.logger.error(f"An error happened while encoding the track data: {e}", exc_info=True)
            return False
        
    def trackExists(self):
        """Checks if the given track already has a register on tracks.json.
        Returns True if the track exists, False otherwise."""

        with open(tracksPath, "r", encoding="utf-8") as file:
            trackData = json.load(file)

        for month, tracks in trackData.items():
            for trackId, trackMetadata in tracks.items():
                if trackId == self.trackId:
                    logConfig.logger.info(f"User tried to insert an existing track:{self.trackId} on tracks.json")
                    return True
                
        else:
            logConfig.logger.info(f"The given track:{self.trackId} doesn't exist on the current data.", exc_info=True)
            return False
    
    def modifyTrackData(self):
        """Modifies the data of the given track.
        Returns True if success, False otherwise."""

        try:
            with open(tracksPath, "w", encoding="utf-8") as file:
                trackData = json.load(file)
            
            trackData[self.month][self.trackId]["name"] = self.name
            trackData[self.month][self.trackId]["author"] = self.author
            trackData[self.month][self.trackId]["phrase"] = self.phrase

            logConfig.logger.info(f"Track data with id:{self.trackId} has been succesfully modified.")
            return True
        except Exception as e:
            logConfig.logger.error(f"An error happened while trying to modify the track's data: {e}", exc_info=True)
            return False
