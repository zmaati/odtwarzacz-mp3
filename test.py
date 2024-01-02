import customtkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox as msg
import pygame
import os
from mutagen.mp3 import  MP3
from math import floor


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


def wybierz_folder():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    buton.configure(text="►", command=zagraj)
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


def kolejna_piosenka():
    global liczba_piosenki, liczba_piosenki_nazwy_pliku
    liczba_piosenki += 1
    liczba_piosenki_nazwy_pliku += 1
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
                        nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
                        running = False
            print("aaa")

    app.after(1, check_event)


gra = 0


def next_song():
    kolejna_piosenka()
    nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
    print("dziala kolejna piosenka")


def previous_song():
    global liczba_piosenki, liczba_piosenki_nazwy_pliku
    liczba_piosenki -= 1
    liczba_piosenki_nazwy_pliku -= 1
    pygame.mixer.music.unload()
    try:
        pygame.mixer.music.load(playlista[liczba_piosenki])
    except IndexError:
        print("koniec listy")
        liczba_piosenki = -1
        liczba_piosenki_nazwy_pliku = 0
    finally:
        pygame.mixer.music.load(playlista[liczba_piosenki])
        zagraj()


def pauza():
    global gra
    pygame.mixer.music.pause()
    gra = 2
    buton.configure(text="►", command=unpauza)


def unpauza():
    pygame.mixer.music.unpause()
    buton.configure(text=" II ", command=pauza)


# MUSIC_END = pygame.USEREVENT
# pygame.mixer.music.set_endevent(MUSIC_END)
# pygame.mixer.music.load(playlista[liczba_piosenki])
# nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])


def klikniecie_listy(event):
    global liczba_piosenki, liczba_piosenki_nazwy_pliku
    selected_item = trv.selection()[0]
    index = trv.index(selected_item)
    print(index)
    liczba_piosenki_nazwy_pliku = index
    liczba_piosenki = index
    nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(playlista[liczba_piosenki])
    zagraj()


def zagraj():
    global gra
    pygame.mixer.music.play()
    buton.configure(text=" II ", command=pauza)
    print(playlista)


trv = ttk.Treeview(
    app, selectmode="browse", height=20, show="headings", columns=columns
)
trv.bind("<<TreeviewSelect>>", klikniecie_listy)

trv.grid(row=0, column=1, padx=10, pady=10)

trv.heading("utwor", text="Tytuł")


nazwa_pliku = tk.CTkLabel(app, textvariable=nazwa_pliku_var)
nazwa_pliku.grid(row=1, column=1)
buton = tk.CTkButton(app, text="►", command=zagraj, width=20, height=30)
buton.grid(row=0, column=0)
next = tk.CTkButton(app, text="⏭️", command=next_song, width=20, height=30)
next.grid(row=1, column=0)
previous = tk.CTkButton(app, text="⏮️", command=previous_song, width=20, height=30)
previous.grid(row=2, column=0)
petla = tk.CTkCheckBox(app, text="Loop", variable=checkbox_var, onvalue=1, offvalue=0)
petla.grid(row=0, column=1)
folder = tk.CTkButton(app, text="Wybierz folder", command=wybierz_folder)
folder.grid(row=0, column=3)

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

audio = MP3("5.mp3")
dlugosc_sekundy = audio.info.length
print(dlugosc_sekundy)


if dlugosc_sekundy<10 :
    dlugosc_sekundy= str(dlugosc_sekundy)
    tk.CTkLabel(app,text="00:0"+dlugosc_sekundy).place(x=150,y=150)      
elif dlugosc_sekundy>10 and dlugosc_sekundy<100:
     dlugosc_sekundy = str(dlugosc_sekundy)
     tk.CTkLabel(app,text="00:"+dlugosc_sekundy).place(x=150,y=150)     
elif dlugosc_sekundy>100 and dlugosc_sekundy<590:
    round(dlugosc_sekundy)
    dlugosc_minuty = dlugosc_sekundy/60
    dlugosc_minuty=floor(dlugosc_minuty)   
    dlugosc_sekundy = dlugosc_sekundy - (dlugosc_minuty*60)
    dlugosc_sekundy = str(dlugosc_sekundy)
    dlugosc_minuty=str(dlugosc_minuty)
    tk.CTkLabel(app,text="0"+dlugosc_minuty[0]+":"+dlugosc_sekundy[0]+dlugosc_sekundy[1]).place(x=150,y=150)
elif dlugosc_sekundy>590:
    dlugosc_minuty = dlugosc_sekundy/60
    dlugosc_minuty=floor(dlugosc_minuty)   
    dlugosc_sekundy = dlugosc_sekundy - (dlugosc_minuty*60)
    floor(dlugosc_sekundy)
    dlugosc_sekundy = str(dlugosc_sekundy)
    dlugosc_minuty=str(dlugosc_minuty)
    print(dlugosc_minuty,"EGIOGJSKGJP")
    print(dlugosc_sekundy,"AAAAAAAAAAAAAA")
    tk.CTkLabel(app,text=dlugosc_minuty[0]+dlugosc_minuty[1]+":"+dlugosc_sekundy[0]+dlugosc_sekundy[1]).place(x=150,y=150)
app.mainloop()
pygame.quit()
