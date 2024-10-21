import json
import spotipy
from spotipy import *
import os
import boto3 
from datetime import datetime

def lambda_handler(event, context):
    
    #Accessing the environment variables
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    
    # creating client credentials manager (authentication)
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    
    # creating a spotify object to access data (authorisation)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Indian top 50 playlist
    playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbLZ52XmnySJg'
    
    # Extracting id
    playlist_uri = playlist_link.split('/')[-1]
    
    spotify_data = sp.playlist_tracks(playlist_uri)
    
    print(spotify_data)
    
    #putting data in s3
    bucket_client = boto3.client('s3')
    
    file_name = "raw_spotify_data" + str(datetime.now()) + ".json"
    
    bucket_client.put_object(
        Bucket = "spotify-etl-bucket-aakif",
        Key = "raw_data/to_processed/" + file_name,
        Body = json.dumps(spotify_data)
        )

