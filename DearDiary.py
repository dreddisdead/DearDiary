import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
import os
import datetime
# from tkinter import font as tkFont


class Entry:
    def __init__(self, date, title, content):
        self.date = date
        self.title = title
        self.content = content

class DiaryApp:
    ### CREATE DIARY UI ON INIT
    def __init__(self):
        # root window
        self.root = tb.Window(title="DearDiary")
        self.root.style.theme_use("superhero")
        self.root.iconbitmap("DearDiary.ico")
        self.root.geometry("320x480")
        self.root.resizable(False, False)
        
        #----------------- FRAMES -----------------#
        self.mainFrame = tb.Frame(self.root)
        self.mainFrame.pack(fill="both", expand=True, padx=10, pady=10)
        self.optionsFrame = tb.Frame(self.root, width=320, height=50, bootstyle="primary")
        self.optionsFrame.pack(fill="both", expand=True, padx=10, pady=10)
        
        #----------------- WIDGETS -----------------#
        self.label1 = tb.Label(self.mainFrame, text="Dear Diary,", font=("Helvetica", 16, "italic"), bootstyle="primary")
        self.label1.pack(pady=5, padx=5, anchor="nw")
        self.entry = ScrolledText(self.mainFrame, height=20, width=40, wrap=WORD, bootstyle=("primary", "rounded"))
        self.entry.pack(pady=5, padx=5, expand=YES, anchor="n")
        # MAIN LOOP
        self.root.mainloop()
        
        
    ### FUNCTIONS
    
        
    
# Run the app
if __name__ == "__main__":
    app = DiaryApp()
    
