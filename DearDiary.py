import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs.dialogs import FontDialog, Messagebox
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
        self.root.geometry("380x560")
        self.root.resizable(False, False)
        self.date = datetime.datetime.now().strftime("%m/%d/%Y")
        self.time = datetime.datetime.now().strftime("%H:%M")
        
        # Empty list to store entries
        self.entries = []
        # Create Entries folder name and create folder if it doesn't exist
        self.folderName = "Entries"
        os.makedirs(self.folderName, exist_ok=True)
        
        
        
        #----------------- FRAMES -----------------#
        self.mainFrame = tb.Frame(self.root)
        self.mainFrame.pack(fill="both", expand=True, padx=10, pady=5)
        self.buttonFrame = tb.Labelframe(self.root, width=120, height=80, text="Options", bootstyle="light")
        self.buttonFrame.pack(padx=10, pady=10, anchor="w")
        
        
        #----------------- WIDGETS -----------------#
        # Date Label 
        self.label1 = tb.Label(self.mainFrame, text=f"Today's Date: {self.date}", font=("Helvetica", 12, "bold", "italic"), bootstyle="light")
        self.label1.pack(pady=5, padx=5, anchor="nw")
        # Entry Title
        self.title = tb.Entry(self.mainFrame, width=15, font=("Helvetica", 12, "bold"))
        self.title.pack(pady=5, padx=5, expand=YES, anchor="n")
        # Place title placeholder
        self.title.insert(0, "Enter Title")
        # Dear Diary Label
        self.label2 = tb.Label(self.mainFrame, text="Dear Diary,", font=("Helvetica", 16, "italic"), bootstyle="light")
        self.label2.pack(pady=5, padx=5, anchor="nw")
        # Diary Entry
        self.entry = ScrolledText(self.mainFrame, height=20, width=40, wrap=WORD, bootstyle=("secondary", "rounded"), font=("Helvetica", 10))
        self.entry.pack(pady=5, padx=5, expand=YES, anchor="n")
        # Buttons
        self.saveButton = tb.Button(self.buttonFrame, text="Save Entry", bootstyle="primary", command=self.saveEntryData)
        self.saveButton.pack(padx=5, pady=5)
        
        #----------------- MAKE DIRECTORY -----------------#
        # Create directory if it doesn't exist
        if not os.path.exists("Entries"):
            os.makedirs("Entries")
        
        # MAIN LOOP
        self.root.mainloop()
        
    ### FUNCTIONS
    def saveEntryData(self):
        # Get entry content
        content = self.entry.get("1.0", "end-1c")
        # Get date
        date = self.date.replace("/", "-")
        # Get time
        time = self.time
        # Get title
        title = self.title.get().strip().replace(" ", "_") # Removes excess whitespace and replaces spaces with underscores
        # Create entry object
        entry = Entry(date, title, content)
        self.entries.append(entry)
        
        # Check that title and content are not empty
        if title == "" or title == "Enter Title" or content == "":
            Messagebox.show_error(title="Error", message="Please enter a title and content for your entry.")
            return
        
        # Save entry to file
        with open(f"{self.folderName}/{title}_{date}.txt", "w") as f:
            f.write(f"Date: {date}\nTime: {time}\nTitle: {title}\nContent: {content}")
        
        # Clear entry and title
        self.clearEntry()
        
        # Let user know entry was saved
        Messagebox.show_info(title="Success", message="Your entry was saved successfully.")
        
        
    def clearEntry(self):
        # Clear entry and title
        self.entry.delete("1.0", "end")
        self.title.delete(0, "end")
        # Place title placeholder
        self.title.insert(0, "Enter Title")
        
        
    
# Run the app
if __name__ == "__main__":
    app = DiaryApp()
    
