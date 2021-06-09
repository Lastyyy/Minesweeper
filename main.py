from functools import partial
from tkinter import *
from tkinter import messagebox
import random

import minesweeperExceptions as msExc

root = Tk()

import pngs
import help

root.geometry("320x410")
root.title("Minesweeper XD")

menuFrame = Frame(root)
menuFrame.grid(row = 0, column = 0)

boardFrame = Frame(root)
boardFrame.grid(row = 4, column = 0)

# Wymiary planszy nxm
wymiaryLabel = Label(menuFrame, text="Wymiary planszy:")
wymiaryLabel.grid(row=0, column=1, columnspan=3)

entryN = Entry(menuFrame, width=3)
entryN.grid(row=1, column=1)
entryM = Entry(menuFrame, width=3)
entryM.grid(row=1, column=3)

nxmLabel = Label(menuFrame, text="x")
nxmLabel.grid(row=1, column=2)

# Liczba min
minsCol = 5

minyStartLabel = Label(menuFrame, text="Miny:")
minyStartLabel.grid(row = 0, column = minsCol)

minyStart = Entry(menuFrame, width=4)
minyStart.grid(row = 1, column = minsCol)

# Liczba oflagowanych min
flagsCol = 10
flaggedBombs = 0
correctlyFlaggedBombs = 0

flaggedBombsLabel = Label(menuFrame, text=str(flaggedBombs))
flaggedBombsLabel.grid(row=1, column = flagsCol)

flagImgLabel = Label(menuFrame, image=pngs.flagImg)
flagImgLabel.grid(row=0, column = flagsCol)

# Liczba min na planszy
bombsCol = 14
bombs = 0
bombsLabel = Label(menuFrame, text = str(bombs))
bombsLabel.grid(row=1, column = bombsCol)
bombsImgLabel = Label(menuFrame, image = pngs.bombsImg)
bombsImgLabel.grid(row = 0, column = bombsCol)

# Lista dwuwymiarowa - pole gry
board = []  # board[x][y] = 1  => bomb
buttons = list()
onScreenValues = list()   # declaring which image user sees on [x][y] field
gameOn = 0
n = 0
m = 0

# Xyzzy
xyzzy = ['x', 'y', 'z', 'z', 'y']
xyzzyMarker = 0

def keyPress(event):
    global xyzzyMarker
    if xyzzyMarker == 5:
        xyzzyMarker = 0
    if event.char.isdigit() == 0 and event.char != "\t":
        help.clearButtons([entryN, entryM, minyStart])
        if event.char == xyzzy[xyzzyMarker] and xyzzyMarker < 5:
            if xyzzyMarker == 4 and gameOn == 1:
                for i in range(0, n):
                    for j in range(0, m):
                        xy= i*n + j
                        if board[i][j] == 1 :#and onScreenValues[xy] > 9 and onScreenValues[xy] < 12:
                            buttons[xy].config(image = pngs.clicked[15])
            xyzzyMarker += 1
        else: xyzzyMarker = 0



root.bind("<Key>", keyPress)



# Function counting bombs near passed field
def checkForBombs():
    print("XD")

def lostGame():
    print("Nice try!")

# Right click-   9= unclicked      10= flag     11= question mark
def rc(x, y, n, event):
    xy = x*n + y
    global flaggedBombs
    global correctlyFlaggedBombs

    if onScreenValues[xy] == 9:
        onScreenValues[xy] = 10
        buttons[xy].config(image = pngs.clicked[10])

        flaggedBombs += 1
        if board[x][y] == 1:
            correctlyFlaggedBombs += 1

    elif onScreenValues[xy] == 10:
        onScreenValues[xy] = 11
        buttons[xy].config(image=pngs.clicked[11])
        flaggedBombs -=1
        if board[x][y] == 1:
            correctlyFlaggedBombs -= 1

    elif onScreenValues[xy] == 11:
        onScreenValues[xy] = 9
        buttons[xy].config(image=pngs.clicked[9])


def clickedField(x, y, n):
    xy = x*n + y

    if onScreenValues[xy] == 9 or onScreenValues[xy] == 11:        # 9= unclicked   11= question mark
        if board[x][y] == 1:
            lostGame()

        else:
            checkForBombs()

# Przycisk NEW GAME
def newGame():
    global n
    global m
    n = int(entryN.get())
    m = int(entryM.get())
    bombsStart = int(minyStart.get())
    try:
        msExc.Game(n, m, bombsStart).CreateGame()
    except msExc.BoardTooSmallException as e:
        messagebox.showwarning("Za mala plansza!", e)
    except msExc.BoardTooBigException as e:
        messagebox.showwarning("Za duza plansza!", e)
    except msExc.BombsAmountNotCorrectException as e:
        messagebox.showwarning("Nieprawidlowa ilosc bomb!", e)
    else:
        for i in boardFrame.winfo_children():
            i.destroy()

        help.clearButtons([entryN, entryM, minyStart])
        global gameOn
        global buttons
        global bombs
        global board
        global onScreenValues
        buttons.clear()
        board.clear()
        onScreenValues.clear()

        bombs = bombsStart
        bombsLabel.config(text = str(bombs))

        for i in range(0, n):
            board.append([0] * m)
            for j in range(0, m):
                buttons.append(Button(boardFrame, image = pngs.clicked[9], command = partial(clickedField, i, j, n)))
                buttons[-1].grid(row = i, column = j)
                buttons[-1].bind("<Button-3>", partial(rc, i, j, n))

                onScreenValues.append(9)
        # Rozmieszczenie min
        bombsToPlace = bombs
        while bombsToPlace > 0:
            nBomb = random.randint(0, n-1)
            mBomb = random.randint(0, m-1)
            if board[nBomb][mBomb] == 0:
                board[nBomb][mBomb] = 1
                bombsToPlace -= 1
        gameOn = 1


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