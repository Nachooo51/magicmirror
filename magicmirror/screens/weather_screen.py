import tkinter as tk

class WeatherScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="black")

        tk.Label(self, text="Tiempo", fg="white", bg="black", font=("Arial", 20)).pack(pady=20)

        tk.Button(self, text="⬅ Volver", command=lambda: app.show("Dashboard")).pack()