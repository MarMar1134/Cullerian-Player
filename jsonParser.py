import os
import json
from pathlib import Path

baseDirectory = Path(__file__).resolve().parent
tracks = baseDirectory / "track_data" / "tracks.json"

def getTrackName(trackPath:str):
    with open(tracks) as f:
        track = json.load(f)
    
    trackRoot, trackNameExtension = os.path.split(trackPath)
    trackName, trackExtension = os.path.splitext(trackNameExtension)

    currentTrack = track[trackName]

    return currentTrack["name"]

def getTrackPath(trackName:str):
    with open(tracks) as f:
        track = json.load(f)
    
    currentTrack = track[trackName]

    return currentTrack["path"]

def getTrackAuthor(trackPath:str):
    with open(tracks) as f:
        track = json.load(f)
    
    trackRoot, trackNameExtension = os.path.split(trackPath)
    trackName, trackExtension = os.path.splitext(trackNameExtension)

    currentTrack = track[trackName]

    return currentTrack["author"]