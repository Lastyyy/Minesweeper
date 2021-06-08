from functools import partial
from tkinter import *
from tkinter import messagebox

import minesweeperExceptions as msExc

root = Tk()

import pngs

root.geometry("330x410")
root.title("Minesweeper XD")

menuFrame = Frame(root)
menuFrame.grid(row = 0, column = 0)

boardFrame = Frame(root)
boardFrame.grid(row = 4, column = 0)

# Wymiary planszy nxm
wymiaryLabel = Label(menuFrame, text="Wymiary planszy:")
wymiaryLabel.grid(row=0, column=1, columnspan=3)

entryN = Entry(menuFrame, width=4)
entryN.grid(row=1, column=1)
entryM = Entry(menuFrame, width=4)
entryM.grid(row=1, column=3)

nxmLabel = Label(menuFrame, text="x")
nxmLabel.grid(row=1, column=2)

# Liczba min
minsCol = 5

minyStartLabel = Label(menuFrame, text="Miny:")
minyStartLabel.grid(row = 0, column = minsCol)

minyStart = Entry(menuFrame, width=3)
minyStart.grid(row = 1, column = minsCol)

# Liczba oflagowanych min
flagsCol = 9
flaggedBombs = 0
flaggedBombsLabel = Label(menuFrame, text=str(flaggedBombs))
flaggedBombsLabel.grid(row=1, column = flagsCol)

flagImgLabel = Label(menuFrame, image=pngs.flagImg)
flagImgLabel.grid(row=0, column = flagsCol)

# Liczba min na planszy
bombsCol = 15
bombs = 0
bombsLabel = Label(menuFrame, text = str(bombs))
bombsLabel.grid(row=1, column = bombsCol)
bombsImgLabel = Label(menuFrame, image = pngs.bombsImg)
bombsImgLabel.grid(row = 0, column = bombsCol)

# Lista dwuwymiarowa - pole gry
board = []
buttons = list()

def rc(event):
    print("OKURWA")


def clickedField(x, y):
    messagebox.showinfo("POZDRO", ":)))" + str(x) + str(y))

# Przycisk NEW GAME
def newGame():
    n = int(entryN.get())
    m = int(entryM.get())
    bombs = int(minyStart.get())
    try:
        msExc.Game(n, m, bombs).CreateGame()
    except msExc.BoardTooSmallException as e:
        messagebox.showwarning("Za mala plansza!", e)
    except msExc.BoardTooBigException as e:
        messagebox.showwarning("Za duza plansza!", e)
    except msExc.BombsAmountNotCorrectException as e:
        messagebox.showwarning("Nieprawidlowa ilosc bomb!", e)
    else:
        for i in boardFrame.winfo_children():
            i.destroy()
        global buttons
        buttons.clear()
        for i in range(0, n):
            global board
            board.append([0] * m)
            for j in range(0, m):
                buttons.append(Button(boardFrame, image = pngs.noBombImg, command = partial(clickedField, i, j)))
                buttons[-1].grid(row = i, column = j)
                buttons[-1].bind("<Button-3>", rc)


newGameButton = Button(root, text = "START A NEW GAME!", command = newGame, height = 2, width = 40)
newGameButton.grid(row = 2, column = 0)

newGameButton.bind("<Button-3>", rc)


# Puste kolumny
col_count, row_count = root.grid_size()
for col in range(0, col_count):
    root.grid_columnconfigure(col, minsize=15)
for row in range(0, row_count):
    root.grid_rowconfigure(row, minsize=8)
root.grid_columnconfigure(0, minsize = 8)

col_count, row_count = menuFrame.grid_size()
for col in range(0, col_count):
    menuFrame.grid_columnconfigure(col, minsize=15)


root.mainloop()