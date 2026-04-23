import tkinter as tk
import requests
import webbrowser


class NewsScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="black")
        self.app = app

        # ⚠️ Pon tu API KEY aquí (https://newsapi.org/)
        self.API_KEY = "TU_API_KEY"

        tk.Label(self, text="📰 Noticias del día",
                 fg="white", bg="black",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(self, text="⬅ Volver",
                  command=lambda: app.show("Dashboard")).pack(pady=5)

        tk.Button(self, text="🔄 Actualizar noticias",
                  command=self.cargar_noticias,
                  bg="#1DB954", fg="black").pack(pady=5)

        # contenedor scroll
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.scroll = tk.Scrollbar(self, orient="vertical",
                                   command=self.canvas.yview)

        self.scroll_frame = tk.Frame(self.canvas, bg="black")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        self.cargar_noticias()

    # -------------------------
    # API NEWS
    # -------------------------
    def cargar_noticias(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        try:
            url = (
                f"https://newsapi.org/v2/top-headlines?"
                f"country=es&language=es&pageSize=10&apiKey={self.API_KEY}"
            )

            data = requests.get(url).json()

            articles = data.get("articles", [])

            if not articles:
                tk.Label(self.scroll_frame,
                         text="No hay noticias",
                         fg="white", bg="black").pack()
                return

            for a in articles:
                self.crear_noticia(a)

        except Exception as e:
            tk.Label(self.scroll_frame,
                     text=f"Error: {e}",
                     fg="red", bg="black").pack()

    # -------------------------
    # UI NOTICIA
    # -------------------------
    def crear_noticia(self, article):
        frame = tk.Frame(self.scroll_frame, bg="#111111", pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        title = article.get("title", "Sin título")
        url = article.get("url", "")

        tk.Label(frame,
                 text=title,
                 fg="white",
                 bg="#111111",
                 wraplength=350,
                 justify="left",
                 font=("Arial", 10, "bold")
                 ).pack(anchor="w")

        tk.Button(frame,
                  text="Leer más",
                  command=lambda u=url: webbrowser.open(u),
                  bg="#1DB954",
                  fg="black"
                  ).pack(anchor="w", pady=5)