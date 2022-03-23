# import tkinter
# from tkinter import filedialog
# import os

# root = tkinter.Tk()
# root.withdraw() #use to hide tkinter window

# currdir = os.getcwd()
# tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
# if len(tempdir) > 0:
#     print("You chose %s" % tempdir)

from tkinter import *
from tkinter import filedialog

import sys
if sys.version_info[0] < 3:
   import Tkinter as Tk
else:
   import tkinter as Tk


def browse_file():
    fname = filedialog.askopenfilename(initialdir="/audioFiles", title="Select a File", filetypes = (("wav files", "*.wav"), ("All files", "*.*")))
    print(fname)

root = Tk.Tk()
root.wm_title("Browser")
broButton = Tk.Button(master = root, text = 'Browse', width = 6, command=browse_file)
broButton.pack(side=Tk.LEFT, padx = 2, pady=2)

Tk.mainloop()