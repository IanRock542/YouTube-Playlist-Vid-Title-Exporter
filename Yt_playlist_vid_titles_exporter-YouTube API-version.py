from urllib import response
from urllib.error import HTTPError
from webbrowser import get
from googleapiclient.discovery import build
from datetime import datetime
import googleapiclient.errors
import os

api_key = os.environ.get('GOOGLE_API_KEY')
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y %H-%M-%S")
youtube = build('youtube', 'v3', developerKey=api_key)

playlist_input = input("Enter a YouTube Playlist: ")
playlist = playlist_input[38:]

def get_titles(playlist_id, pl_titles):
    try:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=500,
            playlistId= playlist_id
        )

        response = request.execute()
    except googleapiclient.errors.HttpError or IndexError as e:
        print("You did not enter a valid playlist.")
        exit(0)
    else:
        for video in range(len(response['items'])):
            pl_titles.append((response['items'][video]['snippet']['title']))
    
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId = playlist_id,
                pageToken = nextPageToken
            ).execute()
            for video in range(len(response['items'])):
                pl_titles.append((response['items'][video]['snippet']['title']))
            nextPageToken = response.get('nextPageToken')

    
    return pl_titles

def get_playlist_title(playlist_id):
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        id= playlist_id,
    )
    response = request.execute()
    pl_title = response['items'][0]['snippet']['title']
    return pl_title

titles = []

titles = get_titles(playlist, titles)
pl_title = get_playlist_title(playlist)
print(f'You just saved the playlist: "{pl_title}" to a text file')



outputfile = pl_title + " " + dt_string +".txt"
with open(outputfile, 'w', encoding="utf-8") as f:
    for video in titles:
        f.write(video + "\n")