import tkinter
from functools import partial
from tkinter import *
from tkinter import messagebox
import random
import queue

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
knownFields = 0
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
    if event.char.isdigit() == 0 and event.char.isalpha() == 1:
        print(event.char)
        help.clearEntries([entryN, entryM, minyStart])
        if event.char == xyzzy[xyzzyMarker] and xyzzyMarker < 5:
            if xyzzyMarker == 4 and gameOn == 1:
                for i in range(0, n):
                    for j in range(0, m):
                        xy= i*n + j
                        if board[i][j] == 1 and onScreenValues[xy] > 8 and onScreenValues[xy] < 12:
                            buttons[xy].config(image = pngs.clicked[15])
            xyzzyMarker += 1
        else: xyzzyMarker = 0


root.bind("<Key>", keyPress)

# Function counting bombs near passed field
def checkForBombs(x, y):
    foundBombs = 0
    global knownFields
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if x+i >= 0 and y+j >= 0 and x+i < m and y+j < n:
                    if board[x+i][y+j] == 1:
                        foundBombs += 1
    # 1. OPCJA Z DISABLOWANIEM PRZYCISKÓW - w celu dzialania odkomentowac opcje nr 3
    #buttons[x*n + y].config(state = DISABLED)

    # 2. OPCJA Z PODMIANA BUTTONS NA IMAGES - w celu dzialania zakomentowac opcje nr 1 oraz 2
    #buttons[x*n + y].destroy()
    #pseudoButton = Label(boardFrame, image=pngs.clicked[foundBombs])
    #pseudoButton.grid(row=x, column=y)

    # 3. WYBRANA PRZEZE MNIE OPCJA - WYLACZENIE FUNKCJONALNOSCI PRZYCISKU, PRZY ZACHOWANIU JEGO WYGLADU
    # - w celu dzialania zakomentowac opcje nr 1 i 2
    buttons[x*n + y].config(image = pngs.clicked[foundBombs])

    onScreenValues[x * n + y] = foundBombs
    knownFields += 1
    if knownFields == n*m - bombs:
        wonGame()
    if foundBombs == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if x + i >= 0 and y + j >= 0 and x + i < m and y + j < n:
                        if onScreenValues[(x+i) * n + (y+j)] > 8:
                            checkForBombs(x+i, y+j)


def lostGame(x, y):
    xy = x*n + y
    global gameOn
    gameOn = 0
    onScreenValues[xy] = 13
    buttons[xy].config(image = pngs.clicked[13])   # clicked field with bomb
    for i in range(0, n):
        for j in range(0, m):
            ij = i*n + j
            if (onScreenValues[ij] == 10 or onScreenValues[ij] == 9) and board[i][j] == 1:  # correct flag or unclicked
                onScreenValues[ij] = 12
                buttons[ij].config(image = pngs.clicked[12])
            elif onScreenValues[ij] == 10 and board[i][j] == 0:   # incorrect flag
                onScreenValues[ij] = 14
                buttons[ij].config(image = pngs.clicked[14])
    messagebox.showinfo("Przegrana!", "Powodzenia nastepnym razem!")

def wonGame():
    global gameOn
    gameOn = 0
    messagebox.showinfo("Zwyciestwo!", "GG WP!")

# Right click-   9= unclicked      10= flag     11= question mark
def rc(x, y, event):
    xy = x*n + y
    global flaggedBombs
    global correctlyFlaggedBombs

    if onScreenValues[xy] == 9:         # unclicked -> flag
        onScreenValues[xy] = 10
        buttons[xy].config(image = pngs.clicked[10])

        flaggedBombs += 1
        flaggedBombsLabel.config(text = flaggedBombs)
        if board[x][y] == 1:
            correctlyFlaggedBombs += 1
        if correctlyFlaggedBombs == flaggedBombs and correctlyFlaggedBombs == bombs:
            wonGame()

    elif onScreenValues[xy] == 10:      # flag -> question mark
        onScreenValues[xy] = 11
        buttons[xy].config(image=pngs.clicked[11])

        flaggedBombs -=1
        flaggedBombsLabel.config(text=flaggedBombs)
        if board[x][y] == 1:
            correctlyFlaggedBombs -= 1
        if correctlyFlaggedBombs == flaggedBombs and correctlyFlaggedBombs == bombs:
            wonGame()

    elif onScreenValues[xy] == 11:      # question mark -> unclicked
        onScreenValues[xy] = 9
        buttons[xy].config(image=pngs.clicked[9])


def clickedField(x, y):
    if gameOn == 1:
        xy = x*n + y

        if onScreenValues[xy] == 9 or onScreenValues[xy] == 11:        # 9= unclicked   11= question mark
            if board[x][y] == 1:
                lostGame(x, y)

            else:
                checkForBombs(x, y)


# START A NEW GAME
def newGame():
    global n
    global m
    try:
        n = int(entryN.get())
        m = int(entryM.get())
        bombsStart = int(minyStart.get())
        msExc.Game(n, m, bombsStart).CreateGame()
    except msExc.BoardTooSmallException as e:
        messagebox.showwarning("Za mala plansza!", e)
    except msExc.BoardTooBigException as e:
        messagebox.showwarning("Za duza plansza!", e)
    except msExc.BombsAmountNotCorrectException as e:
        messagebox.showwarning("Nieprawidlowa ilosc bomb!", e)
    except ValueError as e:
        print("Zadne z pol nie powinno byc puste!")

    else:
        help.clearFrame(boardFrame)

        help.clearEntries([entryN, entryM, minyStart])
        global gameOn
        global knownFields
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
                buttons.append(Button(boardFrame, image = pngs.clicked[9], command = partial(clickedField, i, j)))
                buttons[-1].grid(row = i, column = j)
                buttons[-1].bind("<Button-3>", partial(rc, i, j))

                onScreenValues.append(9)  # adding unclicked fields
        # Placing bombs
        bombsToPlace = bombs
        while bombsToPlace > 0:
            nBomb = random.randint(0, n-1)
            mBomb = random.randint(0, m-1)
            if board[nBomb][mBomb] == 0:
                board[nBomb][mBomb] = 1
                bombsToPlace -= 1
        knownFields = 0
        gameOn = 1

def enter(event):
    newGame()


newGameButton = Button(root, text = "START A NEW GAME!", command = newGame, height = 2, width = 40)
newGameButton.grid(row = 2, column = 0)

root.bind("<Return>", enter)


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