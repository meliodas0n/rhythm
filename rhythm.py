from tkinter import *
import pygame
import os
import wikipedia
import pathlib
import tkinter.font as tkFont
from tkinter import simpledialog
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
from lyrics_extractor import SongLyrics
import Recommenders as Recommenders
import Evaluation as Evaluation
from dotenv import load_dotenv
load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



api_key = "AIzaSyC5dvhCUZawlFulTZfwhSG3mPs979LN8uA"
cse_key = "4a730f5a78fe71353"

root = Tk()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        self.root.resizable(True, True)
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()

        #creating track frame
        trackframe = LabelFrame(self.root, text = "Song Track", font =("times new roman", 16, "italic"), bg = "black", fg = "white", bd = 5, relief = GROOVE, cursor = "arrow")
        trackframe.place(x = 0, y = 0, width = 1440, height = 810)
        songtrack = Label(trackframe, textvariable = self.track, width = 85, font = ("times new roman", 24, "bold"), bg = "black", fg = "gold").grid(row = 0, column = 0, padx = 10, pady = 5)
        trackstatus = Label(trackframe, textvariable=self.status, font=("times new roman", 24, "bold"), bg="black", fg="gold").grid(row=1, column=0, padx=10, pady=5)

        #creating button frame
        buttonframe = LabelFrame(self.root, text="Control Panel", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        buttonframe.place(x=0, y=810, width=1440, height=270)
        playbtn1 = Button(buttonframe, text = "PLAY", command = self.playsong, width = 8, height = 1,font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 0, padx = 20, pady = 5)
        playbtn2 = Button(buttonframe, text="PAUSE", command = self.pausesong, width=8, height = 1,font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 1, padx = 20, pady = 5)
        playbtn3 = Button(buttonframe, text="UNPAUSE", command = self.unpausesong, width=8, height = 1,font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0,column = 2, padx = 20,pady = 5)
        playbtn4 = Button(buttonframe, text="CLOSE", command = self.stopsong, width = 8, height = 1,font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 6, padx = 20, pady = 5)
        playbtn5 = Button(buttonframe, text = "ARTIST", command = self.wiki, width = 8, height = 1, font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 3, padx = 20, pady = 5)
        playbtn6 = Button(buttonframe, text = "RECORD", command = self.voice_rec, font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 5, padx = 20, pady = 5)
        playbtn7 = Button(buttonframe, text = "LYRICS", command = self.show_lyric, font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 4, padx = 20, pady = 5)
        playbtn8 = Button(buttonframe, text = "SUGGESTION", command = self.get_recommendation, font = ("times new roman", 16, "bold"), fg = "navyblue", bg = "gold").grid(row = 0, column = 7, padx = 20, pady = 5)
         

        #creating song list
        songsframe = LabelFrame(self.root, text = "Song List", font = ("times new roman", 18, "bold"), bg = "grey", fg = "white", bd = 5, relief = GROOVE)
        songsframe.place(x = 1440, y = 0, width = 480, height = 675)
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE,font=("times new roman", 12, "bold"), bg="white", fg="navyblue", bd=5, relief=GROOVE)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)

        #for import the location of the songs folder
        path = pathlib.Path("X:\music")
        os.chdir(path)
        songtracks = path.iterdir()
        for track in songtracks:
            self.playlist.insert(END, track)

    def playsong(self):
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("Playing")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()

    def pausesong(self):
        self.status.set("Pause")
        pygame.mixer.music.pause()

    def unpausesong(self):
        self.status.set("Unpause")
        pygame.mixer.music.unpause()

    def stopsong(self):
        self.status.set("Stopped")
        pygame.mixer.music.stop()
        exit(0)

    def wiki(self):
        artist = simpledialog.askstring("Artist", "Please enter the name of the Artist: ")
        name = artist
        wiki_input = wikipedia.page(name)
        msg = wiki_input.content

        pop = Tk()

        fontStyle = tkFont.Font(family = "times new roman", size = 12)

        pop.title(name)

        pop.geometry(f"{pop.winfo_screenwidth()}x{pop.winfo_screenheight()}+0+0")

        w = Message(pop, text = msg)
        w.pack()

    def voice_rec(self):
        fs = 48000
        duration = 2
        print("Recording")
        myrecording = sd.rec(int(duration * fs), samplerate = fs, channels = 2)
        sd.wait()

        return sf.write('my_Audio_file1.flac',  myrecording, fs)
        print("Recorded")

    def show_lyric(self):
        s_name = simpledialog.askstring("SONG NAME", "Please enter the name of the Song: ")
        so_name = s_name

        top = Tk()
        
        fontStyle = tkFont.Font(family = "times new roman", size = 12)

        top.title(so_name)

        top.geometry(f"{top.winfo_screenwidth()}x{top.winfo_screenheight()}+0+0")

        extract_lyrics = SongLyrics(api_key, cse_key)

        data = extract_lyrics.get_lyrics(so_name)

        l = Message(top, text = data.split('\n'))
        l.pack()


    def get_recommendation(self):
        recommendframe = LabelFrame(root, text = "Suggestions", font = ("times new roman", 18, "bold"), bg = "white", fg = "grey", bd = 5, relief = GROOVE)
        recommendframe.place(x = 1440, y = 675, width = 480, height = 405)
        inp = simpledialog.askstring("Song", "Please enter the name of the song : ")
        sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials("8179379b673642bfa740adba6d163b5c", "8b207d4a74984ddf81faf96c5d4c0c55"))
        result = sp.search(q = inp, limit = 1)
        id_list = [result['tracks']['items'][0]['id']]
        recommend = sp.recommendations(seed_tracks = id_list, limit = 9)
        lbl_track_name = Label(master = recommendframe, text = 'Track Name', bg = "white", fg = "black")
        lbl_artist_name = Label(master = recommendframe, text = 'Artist Name', bg = "white", fg = "black")
        lbl_track_name.grid(row = 0, column = 0)
        lbl_artist_name.grid(row = 0, column = 1)
        for idx, track in enumerate(recommend['tracks']):
            lbl_track_name_recommended = Label(master = recommendframe, text = track['name'], fg = "black", bg = "white")
            lbl_track_name_recommended.grid(row = idx + 1, column = 0)
            lbl_artist_name_recommended = Label(master = recommendframe, text = track['artists'][0]['name'], fg = "black", bg = "white")
            lbl_artist_name_recommended.grid(row = idx + 1, column = 1)

    

MusicPlayer(root)
root.mainloop()

