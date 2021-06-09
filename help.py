from tkinter import *
from tkinter import messagebox

def clearButtons(buttons):
    for i in buttons:
        i.delete(0, END)
