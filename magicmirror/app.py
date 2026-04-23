import tkinter as tk
from screens.dashboard import Dashboard
from screens.spotify_screen import SpotifyScreen
from screens.news_screen import NewsScreen
from screens.calendar_screen import CalendarScreen
from screens.weather_screen import WeatherScreen


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mi Dashboard")
        self.root.geometry("400x700")
        self.root.configure(bg="black")

        self.frames = {}

        for F in (Dashboard, SpotifyScreen, NewsScreen, CalendarScreen, WeatherScreen):
            frame = F(self.root, self)
            self.frames[F.__name__] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.show("Dashboard")

    def show(self, name):
        frame = self.frames[name]
        frame.tkraise()

        # 👇 importante para Spotify (y futuras screens con eventos)
        if hasattr(frame, "on_show"):
            frame.on_show()

    def run(self):
        self.root.mainloop()