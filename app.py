# simple_gui.py

from tkinter import *
from tkinter import ttk


def main():
    '''Main function'''
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    
    ttk.Label(frm, text="Anzahl der Wiederholungen:").grid(column=0, row=0)
    var_anzahl = IntVar(value=20)
    entry = ttk.Entry(frm, textvariable=var_anzahl)
    entry.grid(column=1, row=0)
    print(entry.get())
    
    
    ttk.Button(frm, text="Speichern").grid(column=1, row=1)
    ttk.Button(frm, text="Schließen", command=quit).grid(column=1, row=1, sticky=E)
    root.mainloop()

if __name__ == "__main__":
    main()