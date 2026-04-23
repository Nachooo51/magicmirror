import tkinter as tk
from datetime import datetime


class Dashboard(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="black")
        self.app = app

        self.time_label = tk.Label(
            self, fg="white", bg="black", font=("Arial", 16)
        )
        self.time_label.pack(pady=20)

        self.update_time()

        tk.Button(self, text="🎧 Spotify",
                  command=lambda: app.show("SpotifyScreen")).pack(pady=10)

        tk.Button(self, text="📰 Noticias",
                  command=lambda: app.show("NewsScreen")).pack(pady=10)

        tk.Button(self, text="📅 Calendario",
                  command=lambda: app.show("CalendarScreen")).pack(pady=10)

        tk.Button(self, text="☁️ Tiempo",
                  command=lambda: app.show("WeatherScreen")).pack(pady=10)

    def update_time(self):
        now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        self.time_label.config(text=now)
        self.after(1000, self.update_time)