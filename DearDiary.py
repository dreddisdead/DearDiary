import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs.dialogs import FontDialog, Messagebox
import os
import datetime
# from tkinter import font as tkFont


# # Current work in progress
# class LoginScreen:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("DearDiary")
#         self.root.style.theme_use("vapor")
#         self.root.iconbitmap("DearDiary.ico")
#         self.root.geometry("300x500")

#         # Initialize variables
#         self.username_var = tk.StringVar()
#         self.password_var = tk.StringVar()

#         # Create the login screen
#         self.create_login_screen()

#     def create_login_screen(self):
#         # Create widgets
#         username_label = tb.Label(self.root, text="Username:", font=("Helvetica", 12, "bold"), bootstyle="light")
#         username_entry = tb.Entry(self.root, textvariable=self.username_var, width=15, font=("Helvetica", 12, "bold"))
#         password_label = tb.Label(self.root, text="Password:", font=("Helvetica", 12, "bold"), bootstyle="light")
#         password_entry = tb.Entry(self.root, textvariable=self.password_var, show='*', width=15, font=("Helvetica", 12, "bold"))
#         login_button = tb.Button(self.root, text="Login", bootstyle="primary", command=self.check_login)
#         create_account_button = tb.Button(self.root, text="Create Account", bootstyle="primary", command=self.create_account)

#         # Place widgets
#         username_label.pack(pady=5, padx=5, anchor="nw")
#         username_entry.pack(pady=5, padx=5, expand=YES, anchor="n")
#         password_label.pack(pady=5, padx=5, anchor="nw")
#         password_entry.pack(pady=5, padx=5, expand=YES, anchor="n")
#         login_button.pack(padx=5, pady=5)
#         create_account_button.pack(padx=5, pady=5)

#     def check_login(self):
#         username = self.username_var.get()
#         password = self.password_var.get()

#         if not username or not password:
#             Messagebox.show_error(title="Error", message="Please enter a username and password.")
#             return

#         # Here, you should check the username and password against a secure database or file with hashed passwords.
#         # For security reasons, avoid storing plain-text passwords.

#         if self.check_credentials(username, password):
#             self.open_diary_app()
#         else:
#             Messagebox.show_error(title="Error", message="Incorrect username or password.")

#         # Clear password field for security
#         self.password_var.set("")

#     def create_account(self):
#         # Implement your account creation logic here, similar to check_login.
#         # Remember to securely hash and store the password.
#         pass
        
#     def check_credentials(self, username, password):
#         # Implement your credential checking logic here.
#         # This function should return True if the credentials are valid, False otherwise.
#         # You should check the username and hashed password against your database or file.
#         pass
#     def open_diary_app(self):
#         # Implement the logic to open the diary app after successful login.
#         # You can hide the current login screen or destroy it and create a new window for the diary app.
#         pass     
class DiaryApp:
    ### CREATE DIARY UI ON INIT
    def __init__(self):
        # root window
        self.root = tb.Window(title="DearDiary")
        self.root.style.theme_use("vapor")
        self.root.iconbitmap("DearDiary.ico")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.date = datetime.datetime.now().strftime("%m/%d/%Y")
        self.time = datetime.datetime.now().strftime("%H:%M")
        
        
         #----------------- MAKE DIRECTORY -----------------#
        # Create directory if it doesn't exist
        self.folderName = "Entries"
        os.makedirs(self.folderName, exist_ok=True)
        
        # Import existing entries from folder into a list
        self.entries = [entry for entry in os.listdir(self.folderName) if entry.endswith(".txt")]
        
        #----------------- FRAMES -----------------#
        self.mainFrame = tb.Frame(self.root)
        self.mainFrame.pack(fill="both", expand=True, padx=10, pady=5)
        self.entryFrame = tb.Frame(self.root, width=560, height=80, bootstyle="light")
        self.entryFrame.pack(padx=10, pady=10, anchor="w", fill="both", expand=True)
        self.buttonFrame = tb.Labelframe(self.root, width=560, height=80, text="Options", bootstyle="light")
        self.buttonFrame.pack(padx=10, pady=10, anchor="w", fill="both", expand=True)
        
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
        self.entry = ScrolledText(self.entryFrame, height=20, width=50, wrap=WORD, bootstyle=("secondary", "rounded"), font=("Helvetica", 10))
        self.entry.pack(pady=5, padx=5, expand=YES, side="left", anchor="w")
        
        # Treeview of entries
        self.tree = tb.Treeview(self.entryFrame, bootstyle="primary", columns=("Date", "Title"), show="headings")
        self.tree.heading("Date", text="Date", anchor="w")
        self.tree.heading("Title", text="Title", anchor="w")                 
        self.tree.pack(padx=5, pady=10, fill="both", expand=True)
        # Populate treeview with entries
        self.populate_tree_with_entries()
        # Bind double click to treeview to view entry
        self.tree.bind("<Double-1>", lambda event: self.viewEntry())
        
        # Buttons 
        self.saveButton = tb.Button(self.buttonFrame, text="Save New Entry", bootstyle="primary", command=self.saveEntryData)
        self.saveButton.pack(padx=5, pady=5, side="left")
        # Edit Entry Button
        self.editButton = tb.Button(self.buttonFrame, text="Save Changes", bootstyle="primary", command=self.editEntry)
        self.editButton.pack(padx=5, pady=5, side="left")
        # Grey out edit button by default
        self.editButton.config(state="disabled")
        # Delete Entry Button
        self.deleteButton = tb.Button(self.buttonFrame, text="Delete Entry", bootstyle="primary", command=self.deleteEntry)
        self.deleteButton.pack(padx=5, pady=5, side="left")
        # Grey out delete button by default
        self.deleteButton.config(state="disabled")
        # Create new entry button
        self.newEntryButton = tb.Button(self.buttonFrame, text="Create New Entry", bootstyle="primary", command=self.clearEntry)
        self.newEntryButton.pack(padx=5, pady=5, side="left")
        # Disable button by default
        self.newEntryButton.config(state="disabled")
        
        
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

        # Check that title and content are not empty
        if title == "" or title == "Enter_Title" or content == "":
            Messagebox.show_error(title="Error", message="Please enter a title and content for your entry.")
            return
        
        # Save entry to file
        with open(f"{self.folderName}/{title}_{date}.txt", "w") as f:
            f.write(f"Date: {date}\nTime: {time}\nTitle: {title}\nContent: {content}")
        
        # Clear entry and title
        self.clearEntry()
        
        # Let user know entry was saved
        Messagebox.show_info(title="Success", message="Your entry was saved successfully.")
        
        # Populate treeview with entries
        self.populate_tree_with_entries()

          
        
    def clearEntry(self):
        # Enable title entry if it was disabled
        self.title.config(state="normal")
        # Clear entry and title
        self.entry.delete("1.0", "end")
        self.title.delete(0, "end")
        # Place title placeholder
        self.title.insert(0, "Enter Title")
        
        # Enable save button
        self.saveButton.config(state="normal")
        # Disable edit button, create new entry button, and delete button
        self.editButton.config(state="disabled")
        self.newEntryButton.config(state="disabled")
        self.deleteButton.config(state="disabled")
        
    def viewEntry(self):
        # Enable title entry if it was disabled
        self.title.config(state="normal")
        # Open selected entry in editor
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        date = values[0]
        title = values[1]
        with open(f"{self.folderName}/{title}_{date}.txt", "r") as f:
            lines = f.readlines()
            content = lines[3].replace("Content: ", "").strip()
            self.entry.delete("1.0", "end")
            self.entry.insert("1.0", content)
            self.title.delete(0, "end")
            self.title.insert(0, title.replace("_", " "))
        #Disable title entry by default to prevent editing
        self.title.config(state="disabled")   
        
        # Enable edit button and create new entry button
        self.editButton.config(state="normal")
        self.newEntryButton.config(state="normal")
        
        # Until edit button is pressed, disable save button
        self.saveButton.config(state="disabled")
        
        # Enable delete button
        self.deleteButton.config(state="normal")
        
        
    def editEntry(self):
        # Saves edited entry by overwriting original file with new content 
        # and adding edited message with new date and new time
        # Open existing file in read mode to get original content and time
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        date = values[0]
        title = values[1]
        with open(f"{self.folderName}/{title}_{date}.txt", "r") as f:
            lines = f.readlines()
            content = lines[3].replace("Content: ", "").strip()
            time = lines[1].replace("Time: ", "").strip()
            
        
        # Get new entry content
        new_content = self.entry.get("1.0", "end-1c")
        # Get current date
        new_date = self.date.replace("/", "-")
        # Get time
        new_time = datetime.datetime.now().strftime("%H:%M")
        # Get title
        title = self.title.get().strip().replace(" ", "_") # Removes excess whitespace and replaces spaces with underscores
        
        # Check that changes were made
        if new_content == content:
            Messagebox.show_error(title="Error", message="No changes were made to your entry.")
            return
        else: 
            # Overwrite existing file but add edited message with new date and new time
            with open(f"{self.folderName}/{title}_{date}.txt", "w") as f:
                f.write(f"Date: {date}\nTime: {time}\nTitle: {title}\nContent: {new_content}\n\nEdited on {new_date} at {new_time}")
                
        # Clear entry and title
        self.clearEntry()
        
        # Let user know entry was saved
        Messagebox.show_info(title="Success", message="Your changes were saved successfully.")
        
        # Populate treeview with entries
        self.populate_tree_with_entries()
    
    def deleteEntry(self):
        # Deletes selected entry
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        date = values[0]
        title = values[1]
        # Delete file
        os.remove(f"{self.folderName}/{title}_{date}.txt")
        
        # Clear entry and title
        self.clearEntry()
        
        # Let user know entry was deleted
        Messagebox.show_info(title="Success", message="Your entry was deleted successfully.")
        
        # Populate treeview with entries
        self.populate_tree_with_entries()    
    
    def populate_tree_with_entries(self):
        self.tree.delete(*self.tree.get_children()) # Clear tree
        
        # Populate tree with entries
        for filename in os.listdir(self.folderName):
            if filename.endswith(".txt"):
                with open(f"{self.folderName}/{filename}", "r") as f:
                    lines = f.readlines()
                    date = lines[0].replace("Date: ", "").strip()
                    title = lines[2].replace("Title: ", "").strip()
                    self.tree.insert("", "end", values=(date, title))
                  

        
# Run the app
if __name__ == "__main__":
    # test_login = LoginScreen()
    app = DiaryApp()
    
