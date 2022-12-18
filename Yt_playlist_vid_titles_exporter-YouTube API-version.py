from urllib import response
from urllib.error import HTTPError
from webbrowser import get
from googleapiclient.discovery import build
from datetime import datetime
from tkinter import filedialog
import googleapiclient.errors
import os

def choose_dir() -> None:
    """Lets user pick dir to save file to"""

    print("Choose the directory to save the text file to.")
    try:
        os.chdir(filedialog.askdirectory())
    except OSError: #except for user not picking a directory
        dir = os.getcwd()
        print("No directory chosen. Saving to current working directory: {0}".format(dir))

api_key = os.environ.get('GOOGLE_API_KEY') #api key hidden in enviroment var
youtube = build('youtube', 'v3', developerKey=api_key) #sets yt api version


now = datetime.now() #time string to differntiate between playlists with the same title
dt_string = now.strftime("%m-%d-%Y %H-%M-%S")





def get_titles(playlist_id: str, pl_titles: list) -> list:
    """Gets video titles from a playlist and returns them in a list var"""
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
        for video in range(len(response['items'])): #items = videos in playlist
            pl_titles.append((response['items'][video]['snippet']['title']))
    
        nextPageToken = response.get('nextPageToken') #goes to next page of videos

        while nextPageToken: #runs until there are no more pages to loop through
            response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId = playlist_id,
                pageToken = nextPageToken
            ).execute()
            for video in range(len(response['items'])):
                pl_titles.append((response['items'][video]['snippet']['title']))
            nextPageToken = response.get('nextPageToken')

    
    return pl_titles

def get_playlist_title(playlist_id: str) -> str:
    
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        id= playlist_id,
    )
    response = request.execute()
    pl_title = response['items'][0]['snippet']['title']
    return pl_title

def main() -> None:
    """Runs main code to let user pick playlist and save it"""

    choose_dir()

    playlist_input = input("Enter a YouTube Playlist: ")
    playlist = playlist_input[38:] #trims url, so that only playlist id remains
    print("\nPlaylist id: {}".format(playlist) + "\n")

    titles = []

    titles = get_titles(playlist, titles)
    pl_title = get_playlist_title(playlist)
    print(f'You just saved the playlist: "{pl_title}" to a text file')

    outputfile = pl_title + " " + dt_string +".txt"
    with open(outputfile, 'w', encoding="utf-8") as f:
        for video in titles:
            f.write(video + "\n")

    exit = input("Press any key to exit")

if __name__ == "__main__":
    main()    