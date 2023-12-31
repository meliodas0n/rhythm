import customtkinter as ctk


class MusicPlayer(ctk.CTk):
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


if __name__ == "__main__":
    player = MusicPlayer("Rhythm")
    player.mainloop()
