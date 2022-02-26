from pytube import Playlist
from datetime import datetime
from tkinter import filedialog
import os


print("Choose the directory to save the text file to.")
os.chdir(filedialog.askdirectory())

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y %H-%M-%S")

yt_playlist = input("Input the playlist url: ")

try:
    p = Playlist(yt_playlist)
    playlist_title = p.title
    print(f"You just saved the playlist {p.title} to a text file.")
except KeyError as k:
    print("You did not enter a valid playlist: ", k)
else:
    outputfile = p.title + " " + dt_string +".txt"
    with open(outputfile, 'w', encoding="utf-8") as f:
        for video in p.videos:
            f.write(video.title + "\n")
        
