import customtkinter as tk
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo
import pygame
import os

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

liczba_piosenki = 0
liczba_piosenki_nazwy_pliku = 0


def kolejna_piosenka():
    global liczba_piosenki, liczba_piosenki_nazwy_pliku
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(playlista[liczba_piosenki])
    zagraj()
    liczba_piosenki += 1
    liczba_piosenki_nazwy_pliku += 1


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
pygame.mixer.music.load(playlista[liczba_piosenki])
nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])


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
liczba_plikow = 1
for plik in playlista:
    trv.insert("", tk.END, values=plik)
    liczba_plikow += 1

nazwa_pliku = tk.CTkLabel(app, textvariable=nazwa_pliku_var)
nazwa_pliku.grid(row=1, column=1)
buton = tk.CTkButton(app, text="►", command=zagraj, width=20, height=30)
buton.grid(row=0, column=0)
petla = tk.CTkCheckBox(app, text="Loop", variable=checkbox_var, onvalue=1, offvalue=0)
petla.grid(row=0, column=1)

check_event()

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


app.mainloop()
pygame.quit()
