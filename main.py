from tkinter import messagebox
import customtkinter as ctk


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
            appearance_mode if appearance_mode is not None else "System"
        )
        self.color_theme = color_theme if color_theme is not None else "blue"

        ctk.set_appearance_mode(f"{self.appearance_mode}")
        ctk.set_default_color_theme(f"{self.color_theme}")

        self.title(f"{self.name}")
        self.geometry(f"{self.xsize}x{self.ysize}")

        # self.protocol("WM_DELETE_WINDOW", self.on_close)

    # def on_close(self):
    #     self.closed_by_user = True
    #     Utils.on_closing_app(app)
    #
    # def __exit__(self, exc_type=None, exc_value=None, traceback=None):
    #     return self.closed_by_user


class MusicPlayer:
    def __init__(self, app):
        self.app = app

    # def __exit__(self):
    #     return True

    def run(self):
        try:
            self.app.mainloop()
        except Exception as e:
            print(f"Unable to run MusicPlayer due to following \n{e}")

    # def protocol(self, func):
    #     try:
    #         if func == "WM_DELETE_WINDOW":
    #             Utils.on_closing_app(self)
    #     except Exception as e:
    #         raise Exception("Undefined Protocol").with_traceback(e.__traceback__)


class Utils:
    @staticmethod
    def on_closing_app():
        if messagebox.askyesnocancel("QUIT", "Do you want to Quit?"):
            app.destroy()


if __name__ == "__main__":
    app = App("Rhythm")
    app.protocol("WM_DELETE_WINDOW", Utils.on_closing_app)
    player = MusicPlayer(app)
    player.run()
