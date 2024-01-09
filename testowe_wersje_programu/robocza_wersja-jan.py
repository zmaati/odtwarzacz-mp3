import customtkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox as msg
import pygame
import os
from mutagen.mp3 import MP3
from math import floor
import time
import random

app = tk.CTk()
app.geometry("850x450")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)
app.title("Drizzler")
app.iconbitmap("logo.ico")

nazwa_pliku_var = tk.StringVar()
columns = "utwor"

pygame.mixer.init()
pygame.display.init()

playlista = []

MUSIC_END = pygame.USEREVENT

liczba_piosenki = 0
liczba_piosenki_nazwy_pliku = 0


MUSIC_END = pygame.USEREVENT


liczba_piosenki = 0
liczba_piosenki_nazwy_pliku = 0


def wybierz_folder():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    zagraj_przycisk.configure(text="►", command=zagraj)
    dir_path = filedialog.askdirectory(title="Wybierz folder")
    for plik in trv.get_children():
        trv.delete(plik)
    playlista.clear()
    os.chdir(dir_path)
    dir_list = os.listdir(dir_path)
    files = 0
    while files < len(os.listdir(dir_path)):
        if dir_list[files].lower().endswith(".mp3"):
            playlista.append(dir_list[files])
            pygame.mixer.music.set_endevent(MUSIC_END)
            pygame.mixer.music.load(playlista[liczba_piosenki])
            nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
        else:
            print(f"nie obsługiwany plik {dir_list[files]}")
        files += 1
    if len(playlista) == 0:
        nazwa_pliku_var.set("")
        msg.showinfo("Zły folder", "Wybierz folder z przynajmniej jednym plikiem mp3")
    for plik in playlista:
        trv.insert("", tk.END, values=plik)

liczba_piosenki = 0
liczba_piosenki_nazwy_pliku = 0


def kolejna_piosenka():
    global liczba_piosenki, liczba_piosenki_nazwy_pliku
    liczba_piosenki += 1
    liczba_piosenki_nazwy_pliku += 1
    dlugosc_slider.set(0)
    # pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    try:
        pygame.mixer.music.load(playlista[liczba_piosenki])
    except IndexError:
        print("koniec listy")
        liczba_piosenki = 0
        liczba_piosenki_nazwy_pliku = 0
    finally:
        pygame.mixer.music.load(playlista[liczba_piosenki])
        zagraj()


checkbox_var = tk.IntVar()


def check_event():
    global checkbox_var_final
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            running = True
            checkbox_var_final = checkbox_var.get()
            print(checkbox_var_final)
            if checkbox_var_final == 1:
                zagraj()
            elif checkbox_var_final     == 0:
                while running:
                    if len(playlista) > 0:
                        # zagraj_przycisk.configure(text="►", command=zagraj)
                        kolejna_piosenka()
                        nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
                        running = False
            print("aaa")

    app.after(1, check_event)


def next_song():
    kolejna_piosenka()
    nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
    print("dziala kolejna piosenka")


def previous_song():
    global liczba_piosenki, liczba_piosenki_nazwy_pliku
    liczba_piosenki -= 1
    liczba_piosenki_nazwy_pliku -= 1
    nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
    pygame.mixer.music.unload()
    try:
        pygame.mixer.music.load(playlista[liczba_piosenki])
    except IndexError:
        print("koniec listy")
        liczba_piosenki = 0
        liczba_piosenki_nazwy_pliku = 0
    finally:
        pygame.mixer.music.load(playlista[liczba_piosenki])
        zagraj()


def pauza():
    pygame.mixer.music.pause()
    zagraj_przycisk.configure(text="►", command=unpauza)


def unpauza():
    pygame.mixer.music.unpause()
    zagraj_przycisk.configure(text=" II ", command=pauza)


MUSIC_END = pygame.USEREVENT
pygame.mixer.music.set_endevent(MUSIC_END)
# pygame.mixer.music.load(playlista[liczba_piosenki])
# nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])


def klikniecie_listy(event):
    global liczba_piosenki, liczba_piosenki_nazwy_pliku, checkbox_var_final, checkbox_var
    selected_item = trv.selection()[0]
    index = trv.index(selected_item)
    # checkbox_var = 0
    # checkbox_var_final = 0
    print(index)
    liczba_piosenki_nazwy_pliku = index
    liczba_piosenki = index
    # liczba_piosenki_nazwy_pliku -= 1
    # liczba_piosenki -= 1
    nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
    # pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(playlista[liczba_piosenki])
    zagraj()
def zagraj():
    global czas_startu_piosenki, liczba_piosenki,shuffle_checkbox_var
    czas_startu_piosenki = time.time()
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    zagraj_przycisk.configure(text=" II ", command=pauza)

    if shuffle_checkbox_var.get() == 1:
        shuffle()
        petla.configure(state="tkinter.DISABLED")

    audio = MP3(playlista[liczba_piosenki])

    dlugosc_sekundy = audio.info.length
    print(dlugosc_sekundy)

    if dlugosc_sekundy < 10:
        dlugosc_sekundy = round(dlugosc_sekundy)
        dlugosc_sekundy = str(dlugosc_sekundy)
        tk.CTkLabel(app, text="00:0" + dlugosc_sekundy).place(x=700, y=425)
    elif dlugosc_sekundy >= 10 and dlugosc_sekundy < 100:
        dlugosc_sekundy = round(dlugosc_sekundy)
        dlugosc_sekundy = str(dlugosc_sekundy)
        tk.CTkLabel(app, text="00:" + dlugosc_sekundy).place(x=700, y=425)
    elif dlugosc_sekundy >= 100 and dlugosc_sekundy < 590:
        dlugosc_minuty = floor(dlugosc_sekundy / 60)
        dlugosc_sekundy = round(dlugosc_sekundy % 60)
        tk.CTkLabel(
            app,
            text=f"{dlugosc_minuty:02d}:{dlugosc_sekundy:02d}",
        ).place(x=700, y=425)
    elif dlugosc_sekundy >= 590:
        dlugosc_minuty = floor(dlugosc_sekundy / 60)
        dlugosc_sekundy = round(dlugosc_sekundy % 60)
        tk.CTkLabel(
            app,
            text=f"{dlugosc_minuty:02d}:{dlugosc_sekundy:02d}",
        ).place(x=700, y=425)

    pygame.mixer.music.load(playlista[liczba_piosenki])
    pygame.mixer.music.play()
    aktualizuj_timer()

czas_startu_piosenki = 0
timer_var = tk.StringVar()
timer_var.set("00:00")

def aktualizuj_timer():
    global czas_startu_piosenki
    czas_teraz = time.time()
    czas_uplyniety = czas_teraz - czas_startu_piosenki
    czas_uplyniety_minuty = floor(czas_uplyniety / 60)
    czas_uplyniety_sekundy = round(czas_uplyniety % 60)
    czas_formatowany = f"{czas_uplyniety_minuty:02d}:{czas_uplyniety_sekundy:02d}"
    timer_var.set(czas_formatowany)
    app.after(1000, aktualizuj_timer)




def set_music_position(value):
    percentage = float(value) / 100
    current_song = playlista[liczba_piosenki]
    audio = MP3(current_song)
    song_length = audio.info.length
    pygame.mixer.music.set_pos(percentage * song_length)

def update_slider_position():
    if pygame.mixer.music.get_busy():
        current_position = pygame.mixer.music.get_pos() / 1000  # w sekundach
        current_song = playlista[liczba_piosenki]
        audio = MP3(current_song)
        song_length = audio.info.length
        percentage = (current_position / song_length) * 100
        dlugosc_slider.set(percentage)

    app.after(1000, update_slider_position)    



trv = ttk.Treeview(
    app, selectmode="browse", height=20, show="headings", columns=columns
)
trv.bind("<<TreeviewSelect>>", klikniecie_listy)

trv.grid(row=0, column=1, padx=10, pady=10)

trv.heading("utwor", text="Tytuł")


nazwa_pliku = tk.CTkLabel(app, textvariable=nazwa_pliku_var)
nazwa_pliku.place(x=200,y=50)
zagraj_przycisk = tk.CTkButton(app, text="►", command=zagraj, width=20, height=30)
zagraj_przycisk.place(x=150, y=200)
next = tk.CTkButton(app, text="⏭️", command=next_song, width=20, height=30)
next.place(x=180, y=200)
previous = tk.CTkButton(app, text="⏮️", command=previous_song, width=20, height=30)
previous.place(x=113, y=200)
petla = tk.CTkCheckBox(app, text="Loop", variable=checkbox_var, onvalue=1, offvalue=0)
petla.place(x=220, y=204)
folder = tk.CTkButton(app, text="Wybierz folder", command=wybierz_folder)
folder.grid(row=0, column=3)

timer_label = tk.CTkLabel(app, textvariable=timer_var)
timer_label.place(x=450, y=425)

check_event()

# SLIDER GŁOŚNOŚCI

a = 1


def slider_event(value):
    global a
    a = value
    pygame.mixer.music.set_volume(a)


slider = tk.CTkSlider(
    master=app,
    from_=0,
    to=1,
    command=slider_event,
    orientation="vertical",
    height=100,
)
slider.set(1)
slider.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

dlugosc_slider = tk.CTkSlider(
    app,
    from_=0,
    to=100,
    orientation="horizontal",
    fg_color="purple",
    progress_color="blue",
    button_color="Purple",
    state="disabled",
    command=lambda value: set_music_position(value),
)
dlugosc_slider.place(x=495, y=430)
dlugosc_slider.set(0)
app.after(1000, update_slider_position)    

def shuffle():
    global playlista
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    zagraj_przycisk.configure(text="►", command=zagraj)
    random.shuffle(playlista)

shuffle_checkbox_var = tk.IntVar()
shuffle_checkbox = tk.CTkCheckBox(app, text="Shuffle", variable=shuffle_checkbox_var)
shuffle_checkbox.place(x=250, y=204)

app.mainloop()
pygame.quit()
