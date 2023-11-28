import customtkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from playsound import zagraj
from pause import pauza

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
buton2 = tk.CTkButton(app, text="pause", command=pauza)
buton2.grid(row=1, column=0)


app.mainloop()
