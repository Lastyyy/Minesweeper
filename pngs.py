from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image

flagImg = ImageTk.PhotoImage(Image.open("flag.png").resize((17, 17), Image.ANTIALIAS))
bombsImg = ImageTk.PhotoImage(Image.open("bomb.png").resize((21, 21), Image.ANTIALIAS))

fieldSize = 14

# clicked -  0-8= amount of bombs     9= unclicked      10= flag     11= questionMark
#            12= bomb     13= bomb that was clicked      14= incorrectly flagged bomb      15= dark unclicked
clicked = list()
for i in range(16):
    temp = ImageTk.PhotoImage(Image.open(str(i) + ".png").resize((fieldSize, fieldSize), Image.ANTIALIAS))
    clicked.append(temp)