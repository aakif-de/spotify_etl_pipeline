import json
import boto3
import pandas as pd
from io import StringIO
from datetime import datetime

# Method for fetching the album information
def album_information(data):

    almbum_list = []

    for i in data['items']:
        album_ids = i['track']['album']['id']
        album_names = i['track']['album']['name']
        release_dates =i['track']['album']['release_date']
        total_tracks = i['track']['album']['total_tracks']
        external_urls = i['track']['album']['external_urls']['spotify']
        album_dictionary = {
                                'album_ids' : album_ids,
                                'album_names':album_names,
                                'release_dates':release_dates,
                                'total_tracks':total_tracks,
                                'external_urls':external_urls
                            }
        almbum_list.append(album_dictionary)

    return almbum_list
    
# Method for fetching the artist information    
def artist_information(data):

    i = 0
    artist_list = []

    while i < len(data['items']):
        for j in data['items'][i]['track']['artists']:
            artist_id = j['id']
            artist_name = j['name']
            artist_url = j['external_urls']['spotify']
            album_dictionary = {
                                    'artist_id':artist_id,
                                    'artist_name':artist_name,
                                    'artist_url':artist_url
                               }
            artist_list.append(album_dictionary)
        i += 1

    return artist_list
    
# Method for fetching the song information
def track_song_information(data):

    song_list = []

    for i in data['items']:
        song_id = i['track']['id']
        song_name = i['track']['name']
        song_duration = i['track']['duration_ms']
        song_popularity = i['track']['popularity']
        song_added_at = i['added_at']
        song_url = i['track']['external_urls']['spotify']
        song_dictornay = {'song_id':song_id,
                          'song_name':song_name,
                          'song_url':song_url,
                          'song_popularity':song_popularity,
                          'song_added_at':song_added_at.split('T')[0],
                          'song_duration':round(song_duration/60000,2)
                          }
        song_list.append(song_dictornay)
    return song_list
    
def lambda_handler(event, context):

    s3 = boto3.client('s3')
    
    bucket_data = s3.list_objects(
        Bucket="spotify-etl-bucket-aakif",
        Prefix="raw_data/to_processed/")
    
    spotify_data_list = []
    spotify_file_keys_list = []
    
    for files in bucket_data['Contents']:
        file_names = files['Key']
        if file_names.split('.')[-1] == "json":
            raw_data = s3.get_object(Bucket="spotify-etl-bucket-aakif",Key=file_names)
            response = raw_data['Body'].read()
            formatted_json_data = json.loads(response)
            spotify_data_list.append(formatted_json_data)
            spotify_file_keys_list.append(file_names)
            
            
    for data in spotify_data_list:
        almbum_list = album_information(data)
        artist_list = artist_information(data)
        song_list = track_song_information(data)
        
        # Creating DataFrames
        
        album_df = pd.DataFrame.from_dict(almbum_list)
        artist_df = pd.DataFrame.from_dict(artist_list)
        song_df = pd.DataFrame.from_dict(song_list)
        
        # Creating string Io object 
        album_string_io = StringIO()
        
        # Putting the album data into the bucket 
        
        album_file_name = "transformed_data/album_data/album_transformed" + str(datetime.now()) + ".csv"
        album_df.to_csv(album_string_io, index = False)
    
        album_content = album_string_io.getvalue()
        
        s3.put_object(
            Bucket="spotify-etl-bucket-aakif",
            Key=album_file_name,
            Body = album_content)
            
        # Putting the artist data into the bucket 
        
        artist_file_name = "transformed_data/artist_data/artist_transformed" + str(datetime.now()) + ".csv"
        
        artist_string_io = StringIO()  # New StringIO for artist data
        
        artist_df.to_csv(artist_string_io, index = False)
        artist_content = artist_string_io.getvalue()
        
        s3.put_object(
            Bucket="spotify-etl-bucket-aakif",
            Key=artist_file_name,
            Body = artist_content)

        # Putting the song/track data into the bucket
        
        song_file_name = "transformed_data/track_data/songs_transformed" + str(datetime.now()) + ".csv"
        song_string_io = StringIO()  # New StringIO for song data
        
        song_df.to_csv(song_string_io, index = False)
        
        song_content = song_string_io.getvalue()
        
        s3.put_object(
            Bucket="spotify-etl-bucket-aakif",
            Key=song_file_name,
            Body = song_content)
            
    # Now we need to copy the data present in to_prossed folder to processed folder so we don't ending up processing the same data again
    
    for Key in spotify_file_keys_list:
        
        copy_source = {
            'Bucket':"spotify-etl-bucket-aakif",
            'Key': Key
        }
        
        # Making a s3 resource to interact 
        s3_resource = boto3.resource('s3')
        
        # Copying the object in the target location
        s3_resource.meta.client.copy(copy_source,"spotify-etl-bucket-aakif", 'raw_data/processed/' + Key.split('/')[-1])
        
        # now deleting the object form parent location
        s3_resource.Object("spotify-etl-bucket-aakif",Key).delete()
        
        
            

        