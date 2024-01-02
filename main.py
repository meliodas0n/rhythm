import customtkinter as ctk
from helpers import CTkAlertDialog


class App(ctk.CTk):
    def __init__(
        self,
        name: str | None = None,
        size: tuple | None = None,
        appearance_mode: str | None = None,
        color_theme: str | None = None,
    ):
        super().__init__()
        self.name = name if name else "Main"
        self.xsize = size[0] if size else 1920
        self.ysize = size[1] if size else 1080
        self.appearance_mode = (
            appearance_mode if appearance_mode is not None else "system"
        )
        self.color_theme = color_theme if color_theme is not None else "blue"

        ctk.set_appearance_mode(f"{self.appearance_mode}")
        ctk.set_default_color_theme(f"{self.color_theme}")

        self.title(f"{self.name}")
        self.geometry(f"{self.xsize}x{self.ysize}")


class MusicPlayer:
    def __init__(self, app):
        self.app = app

        self.WIDTH = self.app.xsize
        self.HEIGHT = self.app.ysize

        self.left_frame = ctk.CTkFrame(
            self.app,
            width=self.WIDTH * 0.75,
            height=self.HEIGHT,
            fg_color="white",
            corner_radius=0,
            border_color="black",
        )
        self.left_frame.place(
            x=self.WIDTH * 0,
            y=self.HEIGHT * 0,
        )
        self.right_frame = ctk.CTkFrame(
            self.app,
            width=self.WIDTH * 0.25,
            height=self.HEIGHT,
            fg_color="black",
            corner_radius=0,
            border_color="white",
        )
        self.right_frame.place(
            x=self.WIDTH * 0.75,
            y=self.HEIGHT * 0,
        )

        self.track_frame()

    def track_frame(self):
        song_track_frame = ctk.CTkFrame(
            master=self.left_frame,
            width=self.WIDTH * 0.75,
            height=self.HEIGHT * 0.875,
        )
        song_track_frame.place(x=self.WIDTH * 0, y=self.HEIGHT * 0)

    def button_frame(self):
        pass

    def list_frame(self):
        pass

    def recommend_frame(self):
        pass

    def run(self):
        try:
            self.app.mainloop()
        except Exception as e:
            print(f"Unable to run MusicPlayer due to following \n{e}")


class Utils:
    @staticmethod
    def on_closing_app():
        if CTkAlertDialog(title="Close", text="Do you want to Quit?").get_state():
            app.destroy()


if __name__ == "__main__":
    app = App("Rhythm")
    # app.protocol("WM_DELETE_WINDOW", Utils.on_closing_app)
    player = MusicPlayer(app)
    player.run()
