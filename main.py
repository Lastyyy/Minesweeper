from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.geometry("400x400")

# Wymiary planszy nxm
wymiaryLabel = Label(root, text="Wymiary planszy:").grid(row=0, column=0, columnspan=3)

entryN = Entry(root, width=4).grid(row=1, column=0)
entryM = Entry(root, width=4).grid(row=1, column=2)

nxmLabel = Label(root, text="x").grid(row=1, column=1)

# Liczba min
minyStartLabel = Label(root, text="Miny:")
minyStartLabel.grid(row=0, column=6)

minyStart = Entry(root, width=3)
minyStart.grid(row=1, column=6)

# Liczba oflagowanych min
global flaggedBombs
flaggedBombs = 0
flaggedBombsLabel = Label(root, text=str(flaggedBombs))
flaggedBombsLabel.grid(row=1, column=10)
flagImg = ImageTk.PhotoImage(Image.open("flag.png").resize((17, 17), Image.ANTIALIAS))
flagImgLabel = Label(root, image=flagImg)
flagImgLabel.grid(row=0, column=10)

# Liczba min na planszy
bombsCol = 15
global bombs
bombs = 0
bombsLabel = Label(root, text=str(bombs))
bombsLabel.grid(row=1, column = bombsCol)
bombsImg = ImageTk.PhotoImage(Image.open("bomb.png").resize((21, 21), Image.ANTIALIAS))
bombsImgLabel = Label(root, image=bombsImg)
bombsImgLabel.grid(row = 0, column = bombsCol)

# Przycisk NEW GAME
#def newGame():


#newGameButton = Button(root, text = "START A NEW GAME!", command)

root.mainloop()