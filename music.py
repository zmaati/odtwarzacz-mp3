import customtkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
import pygame
import os
from pytube import YouTube
from moviepy.editor import *

app = tk.CTk()
app.geometry("850x450")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)


nazwa_pliku_var = tk.StringVar()
columns = "utwor"
link_var = tk.StringVar()

pygame.mixer.init()
pygame.display.init()


dir_path = filedialog.askdirectory(title="Wybierz folder")
playlista = []

os.chdir(dir_path)
dir_list = os.listdir(dir_path)
files = 0
while files < len(os.listdir(dir_path)):
    if dir_list[files].lower().endswith(".mp3"):
        playlista.append(dir_list[files])
    else:
        print(f"nie obsługiwany plik {dir_list[files]}")
    files += 1

liczba = 1
liczba2 = 0


def kolejna_piosenka():
    global liczba, liczba2
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(playlista[liczba])
    zagraj()
    liczba += 1
    liczba2 += 1


checkbox_var = tk.IntVar()


def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            running = True
            checkbox_var_final = checkbox_var.get()
            print(checkbox_var_final)
            if checkbox_var_final == 1:
                zagraj()
            elif checkbox_var_final == 0:
                while running:
                    if len(playlista) > 0:
                        # buton.configure(text="►", command=zagraj)
                        kolejna_piosenka()
                        nazwa_pliku_var.set(playlista[liczba2])
                        running = False
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
nazwa_pliku_var.set(playlista[liczba2])


def zagraj():
    global gra
    pygame.mixer.music.play()
    buton.configure(text=" II ", command=pauza)
    print(playlista)

def download():
    global folder, queue
    url = link_var.get()
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    download_path = os.path.join(dir_path)
    os.makedirs(download_path, exist_ok=True)
    video.download(download_path)
    print("Downloaded "+yt.title+" to ",download_path)
    filename = os.listdir(download_path)
    for name in filename:
        if name.endswith(".mp4"):
            audio = AudioFileClip(f"{download_path}/{name}")
            nameNomp4 = name.replace(".mp4", "")
            audio.write_audiofile(f"{download_path}/"+nameNomp4+".mp3")
            os.remove(f"{download_path}/"+name)
            return nameNomp4+".mp3"
    print("Converted to mp3")
    for plik in playlista:
        trv.insert("", tk.END, values=plik)


trv = ttk.Treeview(
    app, selectmode="browse", height=20, show="headings", columns=columns
)
trv.grid(row=0, column=1, padx=10, pady=10)

trv.heading("utwor", text="Tytuł")
liczba_plikow = 1
for plik in playlista:
    trv.insert("", tk.END, values=str(liczba_plikow) + "." + plik)
    liczba_plikow += 1

nazwa_pliku = tk.CTkLabel(app, textvariable=nazwa_pliku_var)
nazwa_pliku.grid(row=1, column=1)
buton = tk.CTkButton(app, text="►", command=zagraj, width=20, height=30)
buton.grid(row=0, column=0)
petla = tk.CTkCheckBox(app, text="Loop", variable=checkbox_var, onvalue=1, offvalue=0)
petla.grid(row=0, column=1)

check_event()

a = 0.5


def slider_event(value):
    global a
    a = value
    pygame.mixer.music.set_volume(a)


slider = tk.CTkSlider(master=app, from_=0, to=1, command=slider_event)
slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)



# yt
link = tk.CTkEntry(app, textvariable=link_var).place(relx = 0.6, rely = 0.6, anchor=tk.CENTER)
pobierz = tk.CTkButton(app, text="Dodaj", command=download).place(relx = 0.6, rely = 0.7, anchor=tk.CENTER)


app.mainloop()
pygame.quit()
