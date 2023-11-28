import customtkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from playsound import zagraj
import pygame
app = tk.CTk()
app.geometry("850x450")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

columns = "utwor"

trv = ttk.Treeview(
    app, selectmode="browse", height=20, show="headings", columns=columns
)
trv.grid(row=0, column=1, padx=10, pady=10)

trv.heading("utwor", text="Tytuł")

buton = tk.CTkButton(app, text="►", command=zagraj, width=10)
buton.grid(row=0, column=0)
a = 0

def slider_event(value):
    global a
    a=(value)
    
slider = tk.CTkSlider(master=app, from_=0, to=100, command=slider_event)
slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

pygame.mixer.music.set_volume(a)

app.mainloop()
