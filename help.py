from tkinter import *
from tkinter import messagebox

def clearEntries(entries):
    for i in entries:
        i.delete(0, END)

def clearFrame(frame):
    for i in frame.winfo_children():
        i.destroy()

