import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="black")

        self.root = root
        self.app = app

        # --- SPOTIFY ---
        CLIENT_ID = "TU_CLIENT_ID"
        CLIENT_SECRET = "TU_CLIENT_SECRET"
        REDIRECT_URI = "https://127.0.0.1:8888/callback"
        scope = "user-read-currently-playing user-modify-playback-state playlist-read-private user-read-playback-state"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope,
            cache_path=".cache_spotify"
        ))

        # --- UI ---
        tk.Label(self, text="Spotify Mirror",
                 fg="white", bg="black",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(self, text="⬅ Volver",
                  command=lambda: app.show("Dashboard")).pack()

        self.frame_top = tk.Frame(self, bg="black")
        self.frame_top.pack(fill="both", expand=True)

        self.frame_bottom = tk.Frame(self, bg="black", height=200)
        self.frame_bottom.pack(fill="x", side="bottom")

        # --- PLAYER UI ---
        self.lbl_imagen = tk.Label(self.frame_bottom, bg="black")
        self.lbl_imagen.pack(side="left", padx=10)

        self.lbl_info = tk.Frame(self.frame_bottom, bg="black")
        self.lbl_info.pack(side="left", fill="both", expand=True)

        self.lbl_titulo = tk.Label(self.lbl_info, text="Esperando...",
                                   fg="white", bg="black",
                                   font=("Arial", 10, "bold"))
        self.lbl_titulo.pack()

        self.lbl_artista = tk.Label(self.lbl_info, text="",
                                    fg="#B3B3B3", bg="black")
        self.lbl_artista.pack()

        self.canvas = tk.Canvas(self.frame_bottom, width=250, height=10,
                               bg="gray", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.bar = self.canvas.create_rectangle(
            0, 0, 0, 10, fill="#1DB954", outline=""
        )

        self.mostrar_selector()
        self.actualizar()

    # -------------------------
    # CUANDO SE ABRE LA PANTALLA
    # -------------------------
    def on_show(self):
        # bindings SOLO cuando está visible
        self.root.bind('<Right>', self.next_song)
        self.root.bind('<Left>', self.prev_song)
        self.root.bind('<space>', self.toggle_play)

    # -------------------------
    # SELECTOR
    # -------------------------
    def mostrar_selector(self):
        for w in self.frame_top.winfo_children():
            w.destroy()

        tk.Label(self.frame_top, text="Tus Playlists",
                 fg="white", bg="black",
                 font=("Arial", 14)).pack(pady=20)

        playlists = {
            "Playlist 1": "spotify:playlist:ID1",
            "Playlist 2": "spotify:playlist:ID2",
        }

        for name, uri in playlists.items():
            tk.Button(self.frame_top, text=name,
                      bg="#1DB954", fg="black",
                      command=lambda u=uri: self.play(u),
                      width=25).pack(pady=5)

    # -------------------------
    # PLAY
    # -------------------------
    def play(self, uri):
        try:
            self.sp.start_playback(context_uri=uri)
        except Exception as e:
            print("Error play:", e)

    # -------------------------
    # LOOP UI
    # -------------------------
    def actualizar(self):
        try:
            data = self.sp.current_user_playing_track()

            if data and data.get("item"):
                item = data["item"]

                self.lbl_titulo.config(text=item["name"][:25])
                self.lbl_artista.config(text=item["artists"][0]["name"])

                url = item["album"]["images"][0]["url"]
                img = Image.open(BytesIO(requests.get(url).content))
                img = img.resize((80, 80))

                photo = ImageTk.PhotoImage(img)
                self.lbl_imagen.config(image=photo)
                self.lbl_imagen.image = photo

                prog = data["progress_ms"]
                dur = item["duration_ms"]

                self.canvas.coords(
                    self.bar, 0, 0, (prog / dur) * 250, 10
                )

        except Exception as e:
            print("Error update:", e)

        self.after(2000, self.actualizar)

    # -------------------------
    # CONTROLES
    # -------------------------
    def next_song(self, event=None):
        self.sp.next_track()

    def prev_song(self, event=None):
        self.sp.previous_track()

    def toggle_play(self, event=None):
        try:
            p = self.sp.current_playback()
            if p and p.get("is_playing"):
                self.sp.pause_playback()
            else:
                self.sp.start_playback()
        except:
            pass