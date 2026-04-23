import tkinter as tk
import requests
from datetime import datetime


class WeatherScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="black")
        self.app = app

        # 🌍 ciudades (lat, lon)
        self.cities = {
            "Madrid": (40.4168, -3.7038),
            "Paris": (48.8566, 2.3522),
            "London": (51.5072, -0.1276),
            "Berlin": (52.5200, 13.4050),
            "Rome": (41.9028, 12.4964),
            "New York": (40.7128, -74.0060),
            "Tokyo": (35.6762, 139.6503),
        }

        self.current_city = "Madrid"

        # ---------------- HEADER ----------------
        tk.Label(self, text="🌤 Weather",
                 fg="white", bg="black",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(self, text="⬅ Volver",
                  command=lambda: app.show("Dashboard")).pack()

        # ---------------- CITY SELECTOR ----------------
        self.city_frame = tk.Frame(self, bg="black")
        self.city_frame.pack(pady=10)

        for city in self.cities.keys():
            tk.Button(self.city_frame,
                      text=city,
                      bg="#1DB954",
                      fg="black",
                      command=lambda c=city: self.change_city(c)
                      ).pack(side="left", padx=3)

        # ---------------- WEATHER DISPLAY ----------------
        self.info = tk.Label(self,
                             text="",
                             fg="white",
                             bg="black",
                             font=("Arial", 14))
        self.info.pack(pady=20)

        self.extra = tk.Label(self,
                              text="",
                              fg="#B3B3B3",
                              bg="black")
        self.extra.pack()

        self.update_weather()

    # ---------------- CAMBIAR CIUDAD ----------------
    def change_city(self, city):
        self.current_city = city
        self.update_weather()

    # ---------------- API ----------------
    def get_weather(self, lat, lon):
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&timezone=auto"
        )

        data = requests.get(url).json()
        return data.get("current_weather", {})

    # ---------------- UPDATE ----------------
    def update_weather(self):
        lat, lon = self.cities[self.current_city]
        weather = self.get_weather(lat, lon)

        if not weather:
            self.info.config(text="Error cargando clima")
            return

        temp = weather["temperature"]
        wind = weather["windspeed"]
        code = weather["weathercode"]

        desc = self.translate_weather(code)

        self.info.config(
            text=f"{self.current_city}\n{temp}°C · {desc}"
        )

        self.extra.config(
            text=f"Viento: {wind} km/h\nActualizado: {datetime.now().strftime('%H:%M:%S')}"
        )

        # refresco automático
        self.after(60000, self.update_weather)

    # ---------------- WEATHER CODES ----------------
    def translate_weather(self, code):
        codes = {
            0: "☀️ Despejado",
            1: "🌤 Poco nublado",
            2: "⛅ Parcialmente nublado",
            3: "☁️ Nublado",
            45: "🌫 Niebla",
            48: "🌫 Niebla helada",
            51: "🌦 Llovizna",
            61: "🌧 Lluvia",
            71: "🌨 Nieve",
            80: "🌧 Chubascos",
            95: "⛈ Tormenta"
        }
        return codes.get(code, "🌍 Desconocido")