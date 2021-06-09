import tkinter
from functools import partial
from tkinter import *
from tkinter import messagebox
import random
import help
import minesweeperExceptions as msExc

root = Tk()
root.iconbitmap('img/mine.ico')

import pngs

root.geometry("320x410")
root.title("Minesweeper")

menuFrame = Frame(root)
menuFrame.grid(row = 0, column = 0)

boardFrame = Frame(root)
boardFrame.grid(row = 4, column = 0)

# Size of a board
wymiaryLabel = Label(menuFrame, text="Wymiary planszy:")
wymiaryLabel.grid(row=0, column=1, columnspan=3)

entryN = Entry(menuFrame, width=3)
entryN.grid(row=1, column=1)
entryN.insert(END, '15')
entryM = Entry(menuFrame, width=3)
entryM.grid(row=1, column=3)
entryM.insert(END, '15')

nxmLabel = Label(menuFrame, text="x")
nxmLabel.grid(row=1, column=2)

# Amount of mines
minyCol = 5

minyStartLabel = Label(menuFrame, text="Miny:")
minyStartLabel.grid(row = 0, column = minyCol)


minyStart = Entry(menuFrame, width=4)
minyStart.grid(row = 1, column = minyCol)
minyStart.insert(END, '30')

# Erase the entries checkbox
eraserCol = 7
erase = tkinter.IntVar()

eraserImgLabel = Label(menuFrame, image = pngs.eraserImg)
eraserImgLabel.grid(row = 0, column = eraserCol)

eraserCheckbox = Checkbutton(menuFrame, variable = erase, onvalue = 1, offvalue = 0)
eraserCheckbox.grid(row = 1, column = eraserCol)


# Amount of flagged mines
flagsCol = 11
flaggedBombs = 0
correctlyFlaggedBombs = 0

flaggedBombsLabel = Label(menuFrame, text=str(flaggedBombs))
flaggedBombsLabel.grid(row=1, column = flagsCol)

flagImgLabel = Label(menuFrame, image=pngs.flagImg)
flagImgLabel.grid(row=0, column = flagsCol)

# Amount of mines on a board
bombsCol = 13
bombs = 0
bombsLabel = Label(menuFrame, text = str(bombs))
bombsLabel.grid(row=1, column = bombsCol)
bombsImgLabel = Label(menuFrame, image = pngs.bombsImg)
bombsImgLabel.grid(row = 0, column = bombsCol)

# Lista dwuwymiarowa - pole gry
board = []   # board[x][y] = 1  => bomb
buttons = list()
onScreenValues = list()   # declaring which image user sees on [x][y] field
knownFields = 0
firstClick = 1
gameOn = 0
n = 0
m = 0


# Xyzzy
xyzzy = ['x', 'y', 'z', 'z', 'y']
xyzzyMarker = 0

def xyzzyCheck(event):
    """
    Function, which checks what key was pressed, and if the key was not
    a digit (inserting data into entries) and was the character (we don't want
    enter (used for starting new game), tab (used to move between entries) and other
    special keys to interrupt inserting xyzzy code), then checks if the user is trying to
    activate the xyzzy code. If he inserted code, the bomb fields are changing into darker ones.

    :param event: passed from bind (binded to root),
    event.char is a key that was pressed
    """

    global xyzzyMarker
    global flaggedBombs
    global correctlyFlaggedBombs
    if xyzzyMarker == 5:
        xyzzyMarker = 0
    if event.char.isdigit() == 0 and event.char.isalpha() == 1:
        help.clearEntries([entryN, entryM, minyStart])
        if event.char == xyzzy[xyzzyMarker] and xyzzyMarker < 5:
            if xyzzyMarker == 4 and gameOn == 1:
                for i in range(0, n):
                    for j in range(0, m):
                        xy= i*m + j
                        if board[i][j] == 1 and (onScreenValues[xy] == 9 or onScreenValues[xy] == 11):
                            buttons[xy].config(image = pngs.clicked[15])
                            onScreenValues[xy] = 15
                        elif board[i][j] == 1 and onScreenValues[xy] == 10:
                            buttons[xy].config(image=pngs.clicked[15])
                            onScreenValues[xy] = 15
                            flaggedBombs -= 1
                            flaggedBombsLabel.config(text=flaggedBombs)
                            correctlyFlaggedBombs -= 1
            xyzzyMarker += 1
        elif event.char == 'x':
            xyzzyMarker = 1
        else:
            xyzzyMarker = 0


root.bind("<Key>", xyzzyCheck)

#  Function counting bombs near passed field
def checkForBombs(x, y):
    """
    Checks how many bombs are there in all 8 nearby fields.
    If zero, then all unclicked neighbours of passed field
    are going to be checked with the same function.

    If there are <1, 8> bombs nearby, then the field
    is changing into the right image.
    pngs.clicked[x] is an image of a field, which has x bombs nearby

    :param x: row of passed field
    :param y: column of passed field
    """

    foundBombs = 0
    global knownFields
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if x+i >= 0 and y+j >= 0 and x+i < n and y+j < m:
                    if board[x+i][y+j] == 1:
                        foundBombs += 1

    #  Imitation of disabling button [x][y]
    buttons[x*m + y].config(command = None)
    buttons[x*m + y].config(relief = SUNKEN)
    buttons[x*m + y].config(image = pngs.clicked[foundBombs])

    onScreenValues[x * m + y] = foundBombs
    knownFields += 1
    if knownFields == n*m - bombs:
        wonGame()
    if foundBombs == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if x + i >= 0 and y + j >= 0 and x + i < n and y + j < m:
                        if onScreenValues[(x+i) * m + (y+j)] > 8:
                            checkForBombs(x+i, y+j)


def lostGame(x, y):
    xy = x*m + y
    global gameOn
    gameOn = 0
    onScreenValues[xy] = 13
    buttons[xy].config(image = pngs.clicked[13])   # clicked field with bomb
    for i in range(0, n):
        for j in range(0, m):
            ij = i*m + j
            if (onScreenValues[ij] == 10 or onScreenValues[ij] == 9 or onScreenValues[ij] == 15) and board[i][j] == 1:  # correct flag or unclicked
                onScreenValues[ij] = 12
                buttons[ij].config(image = pngs.clicked[12])
            elif onScreenValues[ij] == 10 and board[i][j] == 0:   # incorrect flag
                onScreenValues[ij] = 14
                buttons[ij].config(image = pngs.clicked[14])
    messagebox.showinfo("Przegrana!", "Powodzenia nastepnym razem!")

def wonGame():
    global gameOn
    gameOn = 0
    messagebox.showinfo("Zwyciestwo!", "Good Game, Well Played!")

# Right click event
def rightClick(x, y, event):
    """
    Commanded function binded to buttons, which are fields on
    a playboard. It checks the onScreenValue for given field,
    and based on that changes it and an image to another one.
    onScreenValues[x] = 9   ->   buttons[x] image = pngs.clicked[9]
    9  = unclicked field
    10 = flagged field
    11 = question marked field
    15 = dark, unclicked field

    While changing into a flagged field or changing the flagged field,
    amount of correctlyFlaggedBombs and flaggedBombs is being changed.

    :param x: row of right clicked field
    :param y: column of right clicked field
    """
    xy = x*m + y
    global flaggedBombs
    global correctlyFlaggedBombs

    #  unclicked -> flag
    if onScreenValues[xy] == 9:
        onScreenValues[xy] = 10
        buttons[xy].config(image = pngs.clicked[10])
        buttons[xy].config(command = None)
        buttons[xy].config(relief = RAISED)

        flaggedBombs += 1
        flaggedBombsLabel.config(text = flaggedBombs)
        if board[x][y] == 1:
            correctlyFlaggedBombs += 1
        if correctlyFlaggedBombs == flaggedBombs and correctlyFlaggedBombs == bombs:
            wonGame()

    #  flag -> question mark
    elif onScreenValues[xy] == 10:
        onScreenValues[xy] = 11
        buttons[xy].config(image=pngs.clicked[11])

        flaggedBombs -=1
        flaggedBombsLabel.config(text=flaggedBombs)
        if board[x][y] == 1:
            correctlyFlaggedBombs -= 1
        if correctlyFlaggedBombs == flaggedBombs and correctlyFlaggedBombs == bombs:
            wonGame()

    #  question mark -> unclicked
    elif onScreenValues[xy] == 11:
        onScreenValues[xy] = 9
        buttons[xy].config(image=pngs.clicked[9])

    #  dark unclicked -> flag
    elif onScreenValues[xy] == 15:
        onScreenValues[xy] = 10
        buttons[xy].config(image=pngs.clicked[10])

        flaggedBombs += 1
        flaggedBombsLabel.config(text=flaggedBombs)
        if board[x][y] == 1:
            correctlyFlaggedBombs += 1
        if correctlyFlaggedBombs == flaggedBombs and correctlyFlaggedBombs == bombs:
            wonGame()


def clickedField(x, y):
    """
    Checks if clicked field should be changed.
    If unclicked, question marked or dark field was clicked,
    function checks if there is a bomb. If the bomb was clicked
    in the first click, bombs are placed again. In the other way,
    if the bomb was clicked the lostGame() function is executed.
    If the field was empty, checkForBombs is executed for the same field.
    If erase
    9  = unclicked field
    11 = question marked field
    15 = dark, unclicked field
    :param x: row of right clicked field
    :param y: column of right clicked field
    """
    if gameOn == 1:
        global firstClick
        xy = x*m + y
                        # 9= unclicked       11= question mark      15 = dark unclicked
        if onScreenValues[xy] == 9 or onScreenValues[xy] == 11 or onScreenValues[xy] == 15:
            if board[x][y] == 1 and firstClick == 1 and bombs != n*m:
                firstClick = 0
                while board[x][y] == 1:
                    help.clearBoard(board, n, m, onScreenValues)
                    bombsToPlace = bombs
                    while bombsToPlace > 0:
                        nBomb = random.randint(0, n - 1)
                        mBomb = random.randint(0, m - 1)
                        if board[nBomb][mBomb] == 0:
                            board[nBomb][mBomb] = 1
                            bombsToPlace -= 1
                for button in buttons:
                    button.config(image = pngs.clicked[9])
                checkForBombs(x, y)

            elif board[x][y] == 1:
                lostGame(x, y)

            else:
                checkForBombs(x, y)
                firstClick = 0


# START A NEW GAME
def newGame():
    """
    Validating entries' data.
    Clearing board and entries (if wanted by user).
    Filling onScreenValues with 9s (unclicked field),
    creating two-dimensional list board for information
    if board[x][y] == 1 (there is a bomb) and creating
    n * m buttons which will create a gameboard.
    Placing bombs in random positions.
    """
    global n, m

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
        if erase.get() == 1:
            help.clearEntries([entryN, entryM, minyStart])

        global correctlyFlaggedBombs, flaggedBombs, gameOn, knownFields
        global buttons, bombs, board, onScreenValues, firstClick

        buttons.clear()
        board.clear()
        onScreenValues.clear()

        bombs = bombsStart
        bombsLabel.config(text = str(bombs))
        onScreenValues = [9 for i in range(n*m)]   # setting up unclicked fields

        for i in range(0, n):
            board.append([0] * m)
            for j in range(0, m):
                buttons.append(Button(boardFrame, image = pngs.clicked[9], command = partial(clickedField, i, j)))
                buttons[-1].grid(row = i, column = j)
                buttons[-1].bind("<Button-3>", partial(rightClick, i, j))

        # Placing bombs
        bombsToPlace = bombs
        while bombsToPlace > 0:
            nBomb = random.randint(0, n-1)
            mBomb = random.randint(0, m-1)
            if board[nBomb][mBomb] == 0:
                board[nBomb][mBomb] = 1
                bombsToPlace -= 1
        knownFields = 0
        flaggedBombs = 0
        flaggedBombsLabel.config(text = str(flaggedBombs))
        correctlyFlaggedBombs = 0
        firstClick = 1
        gameOn = 1

# Pressing 'Enter' as a way to try starting a new game
def enter(event):
    newGame()

root.bind("<Return>", enter)

newGameButton = Button(root, text = "Start!", command =lambda: newGame(), height = 2, width = 40)
newGameButton.grid(row = 2, column = 0)


# Changing size of empty rows and columns
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