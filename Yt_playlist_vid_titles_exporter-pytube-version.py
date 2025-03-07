from pytube import Playlist
from datetime import datetime
from tkinter import filedialog
import os


def choose_dir() -> None:
    """Lets user pick dir to save file to"""

    print("Choose the directory to save the text file to.")
    try:
        os.chdir(filedialog.askdirectory())
    except OSError: # exception for user not picking a directory
        dir = os.getcwd()
        print("No directory chosen. Saving to current working directory: {0}".format(dir))

now = datetime.now()  # time string to differntiate between playlists with the same title
dt_string = now.strftime("%m-%d-%Y %H-%M-%S")

def main() ->None:
    """Runs main code to let user pick playlist and save it"""
    choose_dir()

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

    exit = input("Press any key to exit")

if __name__ == "__main__":
    main()
        
