import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


class CalendarScreen(tk.Frame):
    def __init__(self, root, app):
        super().__init__(root, bg="black")
        self.app = app

        self.file = "events.json"
        self.events = self.load_events()

        # ---------------- UI HEADER ----------------
        tk.Label(self, text="📅 Mi Agenda",
                 fg="white", bg="black",
                 font=("Arial", 18, "bold")).pack(pady=10)

        tk.Button(self, text="⬅ Volver",
                  command=lambda: app.show("Dashboard")).pack(pady=5)

        # ---------------- INPUT ----------------
        self.input_frame = tk.Frame(self, bg="black")
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Evento:",
                 fg="white", bg="black").grid(row=0, column=0)

        self.entry_event = tk.Entry(self.input_frame, width=25)
        self.entry_event.grid(row=0, column=1, padx=5)

        tk.Label(self.input_frame, text="Fecha (DD/MM/YYYY):",
                 fg="white", bg="black").grid(row=1, column=0)

        self.entry_date = tk.Entry(self.input_frame, width=25)
        self.entry_date.grid(row=1, column=1, padx=5)

        tk.Button(self.input_frame, text="➕ Añadir",
                  bg="#1DB954", fg="black",
                  command=self.add_event).grid(row=2, column=0, columnspan=2, pady=5)

        # ---------------- LISTA ----------------
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.scroll = tk.Scrollbar(self, orient="vertical",
                                   command=self.canvas.yview)

        self.list_frame = tk.Frame(self.canvas, bg="black")

        self.list_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

        self.render_events()

    # ---------------- LOAD / SAVE ----------------
    def load_events(self):
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_events(self):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=4)

    # ---------------- ADD EVENT ----------------
    def add_event(self):
        text = self.entry_event.get().strip()
        date = self.entry_date.get().strip()

        if not text or not date:
            messagebox.showwarning("Error", "Completa todos los campos")
            return

        try:
            datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto")
            return

        self.events.append({
            "text": text,
            "date": date
        })

        self.save_events()

        self.entry_event.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

        self.render_events()

    # ---------------- DELETE ----------------
    def delete_event(self, index):
        del self.events[index]
        self.save_events()
        self.render_events()

    # ---------------- RENDER ----------------
    def render_events(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not self.events:
            tk.Label(self.list_frame,
                     text="No hay eventos",
                     fg="gray", bg="black").pack()
            return

        # ordenar por fecha
        try:
            self.events.sort(
                key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y")
            )
        except:
            pass

        for i, ev in enumerate(self.events):
            frame = tk.Frame(self.list_frame, bg="#111111", pady=10)
            frame.pack(fill="x", padx=10, pady=5)

            tk.Label(frame,
                     text=f"{ev['date']} - {ev['text']}",
                     fg="white", bg="#111111",
                     wraplength=300,
                     justify="left").pack(side="left")

            tk.Button(frame,
                      text="🗑",
                      bg="red", fg="white",
                      command=lambda i=i: self.delete_event(i)
                      ).pack(side="right")