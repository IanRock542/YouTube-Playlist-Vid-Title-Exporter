from flask import Flask, request, render_template, send_file
from urllib import response
from urllib.error import HTTPError
from webbrowser import get
from googleapiclient.discovery import build
from datetime import datetime
from tkinter import filedialog
import googleapiclient.errors
import os

app = Flask(__name__)


api_key = os.environ.get('GOOGLE_API_KEY') # api key hidden in enviroment var
youtube = build('youtube', 'v3', developerKey=api_key) # sets yt api version

now = datetime.now() # time string to differntiate between playlists with the same title
dt_string = now.strftime("%m-%d-%Y %H-%M-%S")

def get_titles(playlist_id: str) -> list:
    """Gets video titles from a playlist and returns them in a list var"""
    pl_titles = []
    try:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=500,
            playlistId= playlist_id
        )
        response = request.execute()

        while request:
            for video in range(len(response['items'])): # items = videos in playlist
                pl_titles.append((response['items'][video]['snippet']['title']))
        
            nextPageToken = response.get('nextPageToken') # goes to next page of videos

            while nextPageToken: # runs until there are no more pages to loop through
                response = youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId = playlist_id,
                    pageToken = nextPageToken
                ).execute()
                for video in range(len(response['items'])):
                    pl_titles.append((response['items'][video]['snippet']['title']))
                nextPageToken = response.get('nextPageToken')
    except googleapiclient.errors.HttpError or IndexError as e:
        print("You did not enter a valid playlist.")
        return None
    return pl_titles

def get_playlist_title(playlist_id: str) -> str:
    """Gets playlist's title"""
    
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        id=playlist_id,
    )
    response = request.execute()
    if response.get('items'):
        return response['items'][0]['snippet']['title']
    return "Unknown Playlist"

"""def main() -> None:
    #Runs main code to let user pick playlist and save it
    playlist_input = input("Enter a YouTube Playlist: ")
    playlist = playlist_input[38:] #t rims url, so that only playlist id remains
    print("\nPlaylist id: {}".format(playlist) + "\n")

    titles = []

    titles = get_titles(playlist, titles)
    pl_title = get_playlist_title(playlist)
    print(f'You just saved the playlist: "{pl_title}" to a text file')

    outputfile = pl_title + " " + dt_string +".txt"
    with open(outputfile, 'w', encoding="utf-8") as f:
        for video in titles:
            f.write(video + "\n")

    exit = input("Press any key to exit")"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        if "list=" in playlist_url:
            playlist_id =  playlist_url[38:] # Extract playlist ID
            titles = get_titles(playlist_id)
            playlist_title = get_playlist_title(playlist_id)

            if titles:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{playlist_title}_{timestamp}.txt"
                filepath = os.path.join("downloads", filename)

                os.makedirs("downloads", exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as f:
                    for title in titles:
                        f.write(title + "\n")

                return send_file(filepath, as_attachment=True)
            else:
                return "Invalid Playlist URL or API Limit Reached."
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
