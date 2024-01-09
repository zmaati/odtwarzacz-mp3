**Drizzler - Program do odtwarzania muzyki**

## 1. Wprowadzenie

Drizzler to aplikacja deskoptowa, dzięki której użytkownik może odtwarzać utwory muzyczne zapisane na swoim komputerze - robi to poprzez wybranie odpowiedniego folderu z plikami o formacie ".mp3".

## 2. Wymagania systemowe

Do poprawnego działania programu należy zaimportować następujące bibliolteki:
```
Tkinter
customtkinter
pygame
os
mutagen
math
time
```

## 3. Zmienne

```app``` - Okno tkinter.

```trv``` - Kolumna z utowrami muzycznymi.

```columns``` - Nagłówek kolumny z utworami.



## 4. Funkcje

```wybierz_folder()``` - Funckja, która po wywołaniu otworzy menedżer plików w celu wybrania folderu przez użytkownika.

```python
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
```

```kolejna_piosenka()``` - Funkcja, która po wywołaniu gra następną piosenke według kolejności.

```python
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
```

```check_event()``` - Funkcja, która po wywołaniu sprawdza czy piosenka aktualnie gra, skończyła.

```python
def check_event():
    global checkbox_var_final
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
                        # zagraj_przycisk.configure(text="►", command=zagraj)
                        kolejna_piosenka()
                        nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
                        running = False
            print("aaa")

    app.after(1, check_event)
```

```next_song()``` - Funkcja, która po wywołaniu ustawia tekst dla label'a, w którym jest napisany tytuł, oraz jest wywowyławana funkcja rozpoczynająca następną piosenkę.

```python
def next_song():
    kolejna_piosenka()
    nazwa_pliku_var.set(playlista[liczba_piosenki_nazwy_pliku])
    print("dziala kolejna piosenka")

```

```pauza()``` ```unpauza()``` - Funkcje, które pauzują lub od pauzowują scieżkę dzwiękową.

```python
def pauza():
    pygame.mixer.music.pause()
    zagraj_przycisk.configure(text="►", command=unpauza)


def unpauza():
    pygame.mixer.music.unpause()
    zagraj_przycisk.configure(text=" II ", command=pauza)

```

```klikniecie_listy(event)``` - Funkcja, dzięki której użytkownik ma możliwość wybrania piosenki ze listy (playlisty).

```python
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

```

```zagraj()``` - Funkcja, która po wywołaniu rozpoczyna grać muzykę, w tym również określa długość pliku i wyświetla ją w oknie aplikacji. 

```python
def zagraj():
    pygame.mixer.music.play()
    zagraj_przycisk.configure(text=" II ", command=pauza)
    print(playlista)
    audio = MP3(playlista[liczba_piosenki])

    dlugosc_sekundy = audio.info.length
    print(dlugosc_sekundy)

    if dlugosc_sekundy < 10:
        dlugosc_sekundy = round(dlugosc_sekundy)
        dlugosc_sekundy = str(dlugosc_sekundy)
        tk.CTkLabel(app, text="00:0" + dlugosc_sekundy[0]).place(x=150, y=150)
    elif dlugosc_sekundy > 10 and dlugosc_sekundy < 100:
        dlugosc_sekundy = round(dlugosc_sekundy)
        dlugosc_sekundy = str(dlugosc_sekundy)
        tk.CTkLabel(app, text="00:" + dlugosc_sekundy).place(x=150, y=150)
    elif dlugosc_sekundy > 100 and dlugosc_sekundy < 590:
        round(dlugosc_sekundy)
        dlugosc_minuty = dlugosc_sekundy / 60
        dlugosc_minuty = floor(dlugosc_minuty)
        dlugosc_sekundy = dlugosc_sekundy - (dlugosc_minuty * 60)
        dlugosc_sekundy = str(dlugosc_sekundy)
        dlugosc_minuty = str(dlugosc_minuty)
        tk.CTkLabel(
            app,
            text="0"
            + dlugosc_minuty[0]
            + ":"
            + dlugosc_sekundy[0]
            + dlugosc_sekundy[1],
        ).place(x=150, y=150)
    elif dlugosc_sekundy > 590:
        dlugosc_minuty = dlugosc_sekundy / 60
        dlugosc_minuty = floor(dlugosc_minuty)
        dlugosc_sekundy = dlugosc_sekundy - (dlugosc_minuty * 60)
        floor(dlugosc_sekundy)
        dlugosc_sekundy = str(dlugosc_sekundy)
        dlugosc_minuty = str(dlugosc_minuty)
        print(dlugosc_minuty, "EGIOGJSKGJP")
        print(dlugosc_sekundy, "AAAAAAAAAAAAAA")
        tk.CTkLabel(
            app,
            text=dlugosc_minuty[0]
            + dlugosc_minuty[1]
            + ":"
            + dlugosc_sekundy[0]
            + dlugosc_sekundy[1],
        ).place(x=150, y=150)

```

```slider_event(value)``` - Funkcja służąca do zmieniania głośności dziwięku pliku.

```python
def slider_event(value):
    global a
    a = value
    pygame.mixer.music.set_volume(a)
```

```aktualizuj_timer()``` - Funkcja, która aktualizuje timer (postęp) odtwarzania muzyki w stosunku do jej długości.

```python
def aktualizuj_timer():
    global czas_startu_piosenki
    if pygame.mixer.music.get_busy():
        czas_teraz = time.time()
        czas_uplyniety = czas_teraz - czas_startu_piosenki
        czas_uplyniety_minuty = floor(czas_uplyniety / 60)
        czas_uplyniety_sekundy = round(czas_uplyniety % 60)
        czas_formatowany = f"{czas_uplyniety_minuty:02d}:{czas_uplyniety_sekundy:02d}"
        timer_var.set(czas_formatowany)
    app.after(1000, aktualizuj_timer)
```

```update_slider_position()``` - Funkcja, która ustawia pozycje na pasu postępu podczas odtwarzania muzyki.

```python
def update_slider_position():
    if pygame.mixer.music.get_busy():
        current_position = pygame.mixer.music.get_pos() / 1000  # w sekundach
        current_song = playlista[liczba_piosenki]
        audio = MP3(current_song)
        song_length = audio.info.length
        percentage = (current_position / song_length) * 100
        dlugosc_slider.set(percentage)

    app.after(1000, update_slider_position)
```




## 5. Autorzy & Źródła
```Oprogramowanie``` -> Mateusz Cichosz, Jan Gołębiowski;<br>
```Wygląd aplikacji``` -> Piotr Kowalewski;<br>
```Dokumentacja aplikacji``` -> Krystian Tarnowski<br>

