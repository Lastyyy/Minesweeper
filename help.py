from tkinter import *
from tkinter import messagebox

def clearEntries(entries):
    for i in entries:
        i.delete(0, END)

def clearFrame(frame):
    for i in frame.winfo_children():
        i.destroy()

def clearBoard(board, n, m, onScreenValues):
    for i in range(n):
        for j in range(m):
            board[i][j] = 0
            onScreenValues[i+j] = 9