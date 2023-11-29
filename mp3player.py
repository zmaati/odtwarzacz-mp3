import customtkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
import pygame
import os

app = tk.CTk()
app.geometry("850x450")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

columns = "utwor"

pygame.mixer.init()
pygame.display.init()


dir_path = filedialog.askdirectory(title="Wybierz folder")
playlista = []
os.chdir(dir_path)
dir_list = os.listdir(dir_path)
files = 0
while files < len(os.listdir(dir_path)):
    playlista.append(dir_list[files])
    files += 1


def kolejna_piosenka():
    liczba = 1
    pygame.mixer.music.load(playlista[liczba])
    liczba += 1


def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            running = True
            while running:
                if len(playlista) > 0:
                    # liczba += 1
            print("aaa")

    app.after(1, check_event)


gra = 0


def pauza():
    global gra
    pygame.mixer.music.pause()
    gra = 2
    buton.configure(text="►", command=unpauza)


def unpauza():
    pygame.mixer.music.unpause()
    buton.configure(text=" II ", command=pauza)


MUSIC_END = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_END)
pygame.mixer.music.load(playlista[0])


def zagraj():
    global gra
    pygame.mixer.music.play()
    buton.configure(text=" II ", command=pauza)
    print(playlista)


trv = ttk.Treeview(
    app, selectmode="browse", height=20, show="headings", columns=columns
)
trv.grid(row=0, column=1, padx=10, pady=10)

trv.heading("utwor", text="Tytuł")

buton = tk.CTkButton(app, text="►", command=zagraj, width=20, height=30)
buton.grid(row=0, column=0)

check_event()

a = 1


def slider_event(value):
    global a
    a = value
    pygame.mixer.music.set_volume(a)


slider = tk.CTkSlider(master=app, from_=0, to=1, command=slider_event)
slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


app.mainloop()
pygame.quit()
