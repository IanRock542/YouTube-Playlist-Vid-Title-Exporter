from pytube import Playlist
from datetime import datetime

yt_playlist = input("Input the playlist url: ")
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y %H-%M-%S")

try:
    p = Playlist(yt_playlist)
    playlist_title = p.title
except KeyError as k:
    print("You did not enter a valid playlist. KeyError: ", k)
else:
    outputfile = p.title + " " + dt_string +".txt"
    with open(outputfile, 'w', encoding="utf-8") as f:
        for video in p.videos:
            f.write(video.title + "\n")
        
