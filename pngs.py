from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image

flagImg = ImageTk.PhotoImage(Image.open("flag.png").resize((17, 17), Image.ANTIALIAS))
bombsImg = ImageTk.PhotoImage(Image.open("bomb.png").resize((21, 21), Image.ANTIALIAS))

noBombImg = ImageTk.PhotoImage(Image.open("0.png").resize((14,14), Image.ANTIALIAS))