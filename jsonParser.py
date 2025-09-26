import os
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