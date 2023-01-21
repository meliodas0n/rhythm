#! /usr/bin/python3

"""
  TODO : fix right frame
  TODO : make the song list immersive
  TODO : fix lyrics frame not showing properly - have to adda scroll bar
  TODO : fix recommendation system
  TODO : add volume slider or some shit
  TODO : fix current listening showing the entire instead of the song name
  TODO : FINAL - "make the app executable"
"""

from tkinter import *
import pygame
import os
import subprocess
import wikipedia
import pathlib
import tkinter.font as tkFont
from tkinter import simpledialog
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
from lyrics_extractor import SongLyrics
from dotenv import load_dotenv
load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment

#keys for lyrics extractor
API_KEY = "AIzaSyAwNAeNy9OrcWkQFYMTh0gVmEQl1lB3FXo"
CSE_KEY = "604928c7439f74806"

root = Tk()

WIDTH = 1920
HEIGHT = 1080
# WIDTH = root.winfo_screenwidth()
# HEIGHT = root.winfo_screenheight()

PATH = pathlib.Path("/home/shadow/code/projects/rhythm/music/")

class MusicPlayer:
  def __init__(self, root):
    self.root = root
    self.root.title("Music Player")
    self.root.geometry(f"{WIDTH}x{HEIGHT}+0+0")
    self.root.resizable(True, True)
    pygame.init()
    pygame.mixer.init()
    self.track = StringVar()
    self.status = StringVar()

    leftframe = Frame(root)
    leftframe.place(x = WIDTH * 0, y = HEIGHT * 0, width = WIDTH * 0.75, heigh = HEIGHT)
    
    rightframe = Frame(root)
    rightframe.place(x = WIDTH * 0.75, y = HEIGHT * 0, width = WIDTH * 0.25, height = HEIGHT)
    
    #creating track frame
    trackframe = LabelFrame(leftframe, text = "Song Track", font =("times new roman", 16, "italic"), bg = "black", fg = "white",  relief = GROOVE, cursor = "arrow")
    trackframe.place(x = WIDTH * 0, y = HEIGHT * 0, width = WIDTH * 0.75, height = HEIGHT * 0.875)
    songtrack = Label(trackframe, textvariable = self.track, width = 75, font = ("times new roman", 24, "bold"), bg = "black", fg = "white").grid(row = 0, column = 0, padx = 10, pady = 5)
    trackstatus = Label(trackframe, textvariable=self.status, font=("times new roman", 24, "bold"), bg="black", fg="white").grid(row=1, column=0, padx=10, pady=5)
    
    #creating button frame
    buttonframe = LabelFrame(leftframe, text="Control Panel", font=("times new roman", 15, "italic"), bg="white", fg="black", relief=GROOVE)
    buttonframe.place(x= WIDTH * 0, y= HEIGHT * 0.875, width = WIDTH, height = HEIGHT * 0.25)
    playbtn1 = Button(buttonframe, text = "PLAY", command = self.playsong,  font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 0, padx = 20, pady = 5)
    playbtn2 = Button(buttonframe, text="PAUSE", command = self.pausesong, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 1, padx = 20, pady = 5)
    playbtn3 = Button(buttonframe, text="UNPAUSE", command = self.unpausesong, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0,column = 2, padx = 20,pady = 5)
    playbtn4 = Button(buttonframe, text="STOP", command = self.stopsong, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 3, padx = 20, pady = 5)
    playbtn5 = Button(buttonframe, text = "ARTIST", command = self.wiki, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 4, padx = 20, pady = 5)
    playbtn6 = Button(buttonframe, text = "RECORD", command = self.voice_rec, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 5, padx = 20, pady = 5)
    playbtn7 = Button(buttonframe, text = "LYRICS", command = self.show_lyric, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 6, padx = 20, pady = 5)
    playbtn8 = Button(buttonframe, text = "SUGGESTION", command = self.get_recommendation, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 7, padx = 20, pady = 5)
    playbtn9 = Button(buttonframe, text = "CLOSE", command = self.close, font = ("times new roman", 16, "bold italic"), fg = "navyblue", bg = "silver").grid(row = 0, column = 8, padx = 20, pady = 5)
    
    #creating song list
    songsframe = LabelFrame(rightframe, text = "Song List", font = ("times new roman", 18, "italic"), bg = "black", fg = "white", relief = GROOVE)
    songsframe.place(x = WIDTH * 0.75, y = HEIGHT * 0, width = WIDTH * 0.25, height = HEIGHT * 0.5)
    scrol_y = Scrollbar(songsframe, orient=VERTICAL)
    self.playlist = Listbox(songsframe, yscrollcommand = scrol_y.set, selectbackground = "blue", selectmode = SINGLE, font = ("times new roman", 12, "italic"), bg = "black", fg = "white") #  bd = 5, relief = GROOVE
    scrol_y.pack(side=RIGHT, fill=Y)
    scrol_y.config(command=self.playlist.yview)
    self.playlist.pack(side = BOTTOM, fill=BOTH)

    #for import the location of the songs folder
    os.chdir(PATH)
    songtracks = PATH.iterdir()
    for track in songtracks:
      if str(track).endswith('.mp3'):
        self.playlist.insert(END, track)


  # def playsong(self):
  #   current_song = self.playlist.get(ACTIVE)
  #   self.track.set(current_song)
  #   self.status.set("Playing")
  #   playable_song = current_song.split('.')[0]
  #   if os.path.exists(f'{playable_song}.ogg'):
  #     playable_song = f'{playable_song}.ogg'
  #     pygame.mixer.music.load(playable_song)
  #     pygame.mixer.music.play()
  #   else:
  #     try:
  #       s = subprocess.call(['ffmpeg', '-i', current_song, f'{playable_song}.ogg'])
  #       if s == 0:
  #         playable_song = f'{playable_song}.ogg'
  #         pygame.mixer.music.load(playable_song)
  #         pygame.mixer.music.play()
  #       else:
  #         print('u suck - conversion failed')
  #     except Exception as e:
  #       print(e)    

  def playsong(self) -> None:
      current_song = self.playlist.get(ACTIVE)
      print(current_song)
      self.track.set(current_song)
      self.status.set("Playing")
      s = subprocess.call(['ftransc', '-f', 'ogg', current_song])
      playable_song = current_song.split('.')[0]
      print(playable_song)
      try:
        if s == 0:
          pygame.mixer.music.load(f'{playable_song}.ogg')
          pygame.mixer.music.play()
      except Exception as e:
        print(f'{e}')

  def pausesong(self):
    self.status.set("Pause")
    pygame.mixer.music.pause()

  def unpausesong(self):
    self.status.set("Unpause")
    pygame.mixer.music.unpause()

  def stopsong(self):
    self.status.set("Stopped")
    pygame.mixer.music.stop()
  
  def close(self):
    test = os.listdir(PATH)
    for item in test:
      if item.endswith('ogg'):
        os.remove(os.path.join(PATH, item))
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
    result = StringVar()
    s_name = simpledialog.askstring("SONG NAME", "Please enter the name of the Song: ")
    so_name = s_name
    if so_name:
      extract_lyrics = SongLyrics(API_KEY, CSE_KEY)
      data = extract_lyrics.get_lyrics(so_name)
      msg = data['lyrics']
      result.set(msg)
      lyricframe = LabelFrame(self.root, text = "Lyrics", font = ("times new roman", 10, "italic"), bg = "black", fg = "white", relief = GROOVE)
      lyricframe.place(x = WIDTH * 0, y = HEIGHT * 0.125, width = WIDTH * 0.75, height = HEIGHT * 0.75)
      t = Label(lyricframe, textvariable = result, bg = "black", fg = "white")        
      t.pack()

  def get_recommendation(self):
    recommendframe = LabelFrame(self.root, text = "Suggestions", font = ("times new roman", 18, "bold"), bg = "white", fg = "black", relief = GROOVE)
    recommendframe.place(x = WIDTH * 0.75, y = HEIGHT * 0.5, width = WIDTH * 0.25, height = HEIGHT * 0.5)
    inp = simpledialog.askstring("Song", "Please enter the name of the song : ")
    if inp:
      sp = spotipy.Spotify(client_credentials_manager = SpotifyClientCredentials("8179379b673642bfa740adba6d163b5c", "8b207d4a74984ddf81faf96c5d4c0c55"))
      result = sp.search(q = inp, limit = 1)
      id_list = [result['tracks']['items'][0]['id']]
      recommend = sp.recommendations(seed_tracks = id_list, limit = 20)
      lbl_track_name = Label(master = recommendframe, text = 'Track Name', bg = "white", fg = "black")
      lbl_artist_name = Label(master = recommendframe, text = 'Artist Name', bg = "white", fg = "black")
      lbl_track_name.grid(row = 0, column = 0)
      lbl_artist_name.grid(row = 0, column = 1)
      for idx, track in enumerate(recommend['tracks']):
        lbl_track_name_recommended = Label(master = recommendframe, text = track['name'], fg = "black", bg = "white")
        lbl_track_name_recommended.grid(row = idx + 1, column = 0)
        lbl_artist_name_recommended = Label(master = recommendframe, text = track['artists'][0]['name'], fg = "black", bg = "white")
        lbl_artist_name_recommended.grid(row = idx + 1, column = 1)

def on_closing():
  if messagebox.askokcancel("QUIT", "Do you want to Quit?"):
    test = os.listdir(PATH)
    for item in test:
      if item.endswith('ogg'):
        os.remove(os.path.join(PATH, item))
    root.destroy()

MusicPlayer(root)
root.protocol('WM_DELETE_WINDOW', on_closing)
root.mainloop()
