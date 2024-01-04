import customtkinter as ctk
from helpers import CTkAlertDialog


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


class Utils:
  @staticmethod
  def on_closing_app():
    if CTkAlertDialog(title = "Close", text = "Do you want to Quit?").get_state():
      app.destroy()


if __name__ == "__main__":
  app = App("Rhythm")
  app.protocol("WM_DELETE_WINDOW", Utils.on_closing_app)
