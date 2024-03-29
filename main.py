import os

import customtkinter as ctk
from helpers import CTkAlertDialog
import tkinter as tk

class App(ctk.CTk):
  def __init__(self, name = None, size = None, appearance_mode = None, color_theme = None):
    # ctk init 
    super().__init__()

    # app parameters
    self.name = name if name else "Main"
    self.xsize = size[0] if size else 1920
    self.ysize = size[1] if size else 1080
    self.appearance_mode = appearance_mode if appearance_mode is not None else "system"
    self.color_theme = color_theme if color_theme is not None else "blue"
    
    # app theme settings
    ctk.set_appearance_mode(f"{self.appearance_mode}")
    ctk.set_default_color_theme(f"{self.color_theme}")
    
    # app title/resolution settings
    self.title(f"{self.name}")
    self.geometry(f"{self.xsize}x{self.ysize}")
    
    # grid setup
    self.grid_rowconfigure(3, weight = 1)
    self.grid_columnconfigure(3, weight = 1)

class MusicPlayer():
  def __init__(self, app, music_dir):
    # assign app to musicplayer
    self.app = app
    self.music_dir = music_dir

    # get resolution of app as width and height
    self.WIDTH = self.app.xsize
    self.HEIGHT = self.app.ysize

    # left side frame to place the song-track and control panel to control the music
    # self.left_frame = ctk.CTkFrame(self.app, width = self.WIDTH * 0.75, height = self.HEIGHT, fg_color = 'white', corner_radius = 0, border_color = 'black')
    # self.left_frame.place(x = self.WIDTH * 0, y = self.HEIGHT * 0)

    # right side frame for song list and recommendation
    # self.right_frame = ctk.CTkFrame(self.app, width = self.WIDTH * 0.25, height = self.HEIGHT, fg_color = 'white', corner_radius = 0, border_color = 'black')
    # self.right_frame.place(x = self.WIDTH * 0.75, y = self.HEIGHT * 0)

    # call individual frames on the app
    self.track_frame()
    self.control_panel()
    self.list_frame()
    self.recommend_frame()

  # frame for song track
  def track_frame(self):
    song_track_frame = ctk.CTkFrame(self.app, width = self.WIDTH * 0.75, height = self.HEIGHT * 0.875, fg_color = "black", corner_radius = 0, border_color = "white")
    song_track_frame.place(x = self.WIDTH * 0, y = self.HEIGHT * 0)
    song_track_frame = Utils.label_frame(song_track_frame, label = "Song Track", color = "white")
    return song_track_frame

  # frame for conttol panel to control the music
  def control_panel(self):
    control_panel_frame = ctk.CTkFrame(self.app, width = self.WIDTH * 0.75, height = self.HEIGHT * 0.125, fg_color = "white", corner_radius = 0, border_color = "black")
    control_panel_frame.place(x = self.WIDTH * 0, y = self.HEIGHT * 0.875)
    control_panel_frame = Utils.label_frame(control_panel_frame, label = "Control Panel", color = "black")
    return control_panel_frame

  # song list frames
  def list_frame(self):
    song_list_frame = ctk.CTkFrame(self.app, width = self.WIDTH * 0.25, height = self.HEIGHT * 0.5, fg_color = "white", corner_radius = 0, border_color = "black")
    song_list_frame.place(x = self.WIDTH * 0.75, y = self.HEIGHT * 0)
    song_list_frame = Utils.label_frame(song_list_frame, label = "Song List", color = "black")
    self.playlist = tk.Listbox(song_list_frame, selectmode = tk.SINGLE, width = int(self.WIDTH * 0.05), height = int(self.HEIGHT * 0.1))
    songtracks = Utils.list_songs(self.music_dir)
    for tracks in songtracks:
      if str(tracks).endswith(".mp3"):
        self.playlist.insert(tk.END, tracks)
    # self.playlist.pack(side = tk.TOP, fill = tk.BOTH)
    self.playlist.place(x = self.WIDTH * 0.76, y = self.HEIGHT * 0.03)
    return song_list_frame

  # recommendatiom frame
  def recommend_frame(self):
    song_recommendation_frame = ctk.CTkFrame(self.app, width = self.WIDTH * 0.25, height = self.HEIGHT * 0.5, fg_color = "black", corner_radius = 0, border_color = "white")
    song_recommendation_frame.place(x = self.WIDTH * 0.75, y = self.HEIGHT * 0.5)
    song_recommendation_frame = Utils.label_frame(song_recommendation_frame, label = "Recommendations", color = "white")
    return song_recommendation_frame

  # run the app
  def run(self):
    try:
      self.app.mainloop()
    except Exception as e:
      print(f"Unable to run Rhythm due to following: \n{e}")

class Utils:
  @staticmethod
  def on_closing_app():
    if CTkAlertDialog(title = "Close", text = "Do you want to Quit?").get_state():
      app.destroy()
    
  @staticmethod
  def label_frame(frame, label = None, color = "black"):
    return ctk.CTkLabel(frame, text = label, text_color = color, font = ctk.CTkFont(size=36, weight="bold")).place(x=0, y=0)

  @staticmethod
  def list_songs(PATH):
    songs_list = []
    for root, dirs, files in os.walk(PATH):
      for filename in files:
        if os.path.splitext(filename)[1] == ".mp3":
          songs_list.append(str(os.path.join(root, filename)).split(PATH)[-1])
    return songs_list

if __name__ == "__main__":
  app = App("Rhythm")
  # app.protocol("WM_DELETE_WINDOW", Utils.on_closing_app)
  player = MusicPlayer(app, "~/dev/rhythm/music/")
  player.run()
