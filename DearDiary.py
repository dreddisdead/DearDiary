import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import os
import datetime
from tkinter import font as tkFont
from ttkthemes import ThemedTk

class Entry:
    def __init__(self, date, title, content):
        self.date = date
        self.title = title
        self.content = content

class DiaryApp:
    def __init__(self):
        self.root = ThemedTk()
        self.root.title("DearDiary")
        # Set size of window
        self.root.geometry("1080x560")
        
        # Change the icon of the window using the iconbitmap() method
        self.icon_path = "pen.ico"  # path to icon file
        self.root.iconbitmap(self.icon_path)
        
        self.entry_list = []
        self.entries_folder = "diary_entries"
        
        # Create the entries folder if it doesn't exist
        os.makedirs(self.entries_folder, exist_ok=True)
        
        
        self.create_ui()
        
        self.root.mainloop()
        
    # Change style
    def change_theme(self, theme):
        style = ttk.Style(self.root)
        # Change style
        style.theme_use(theme)
        
        
    def change_font(self, *args):
        selected_font = self.font_var.get()
        font = tkFont.Font(family=selected_font, size=12)  # Change size as needed
        self.entry_text.config(font=font) 
        
    
    # function to store current selected font
    def get_font(self):
        return self.font_var.get() 
    
    def view_entry_tab(self):
        self.view_entry_notebook = ttk.Notebook(self.root)
        self.view_entry_notebook.grid(row=0, column=1, padx=10, pady=10)  
        
        # Create a frame for the notebook
        self.view_entry_frame = tk.Frame(self.view_entry_notebook, width=500, height=500)
        
        
        self.view_entry_frame.pack(fill="both", expand=1)
        # Put treeview inside this frame
        self.tree = ttk.Treeview(self.view_entry_frame, columns=("Date", "Title"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Title", text="Title")
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        
        # Populate the treeview with existing entries
        self.populate_treeview_with_entries()
        # Bind double click to show selected entry
        self.tree.bind("<Double-1>", self.show_selected_entry)
        
        
        # Add the frames to the notebook
        self.view_entry_notebook.add(self.view_entry_frame, text="View Entries")
        
    def date_and_title(self):
        # Create a frame to hold the date and title entry fields
        self.date_and_title_frame = tk.Frame(self.root)
        self.date_and_title_frame.grid(row=0, column=0, padx=10, pady=5)
        
        # Place the date and title entry fields in the frame
        self.date_entry = ttk.Entry(self.date_and_title_frame)
        self.date_entry.grid(row=0, column=0, padx=10, pady=5)
        # Automatically set the current date in the date_entry field
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_entry.insert(0, self.current_date)
        
        # Create title entry with placeholder text
        self.title_entry = ttk.Entry(self.date_and_title_frame)
        self.title_entry.insert(0, "Enter Title")
        self.title_entry.grid(row=1, column=0, padx=10, pady=5)
        
    def entry_text(self):
        # Create a frame to hold the entry text field
        self.entry_text_frame = tk.Frame(self.root)
        self.entry_text_frame.grid(row=1, column=0, padx=10, pady=5)
        
        # Place the entry text field in the frame
        self.entry_text = scrolledtext.ScrolledText(self.entry_text_frame, height=15, width=60) # Adjust height and width as needed
        self.entry_text.grid(row=0, column=0, padx=10, pady=5)
        self.entry_text.config(wrap=tk.WORD, font=('Arial', 12))
              
    
    def create_ui(self):
        # Configure the root window grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        
        
        # Create a menu bar with options
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # Close or force quit
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Close", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        # Choose a theme
        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Themes", menu=self.theme_menu)
         
        # see included themes
        self.our_themes = self.root.get_themes()
        # Loop through themes and add them to the menu
        for theme in self.our_themes:
            self.theme_menu.add_radiobutton(label=theme, command=lambda theme=theme: self.change_theme(theme))
 
 
        # Call the date_and_title function
        self.date_and_title()
        
        # Call the entry_text function
        self.entry_text()
        
        add_button = ttk.Button(self.root, text="Add Entry", command=self.add_entry, width=20)
        add_button.grid(row=3, column=0, padx=10, pady=5)
        
        # Create a font selection dropdown
        self.font_var = tk.StringVar()
        self.font_var.set("Arial")  # Set a default font
        self.list_of_fonts = ["Arial", "Times New Roman", "Courier New", "Calibri", "Comic Sans MS", "Verdana", "Georgia", "Impact", "Lucida Console", "Tahoma", "Trebuchet MS"]
        self.font_dropdown = ttk.OptionMenu(self.root, self.font_var, *self.list_of_fonts)
        self.font_dropdown.grid(row=4, column=0, padx=10, pady=5)
         
        # Add a trace to call change_font when the font selection changes
        self.font_var.trace_add('write', self.change_font)
        
        # Call the view_entry_tab function
        self.view_entry_tab()
        
             
    def add_entry(self):
        date = self.date_entry.get()
        title = self.title_entry.get().strip() #removes spaces from front and end of text
        content = self.entry_text.get("1.0", "end-1c")
        font = self.get_font()
        
        # Automatically set the current date in the date_entry field
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, current_date)
        
        if title == "Enter Title" or not content or title == "":
            messagebox.showwarning("Incomplete Entry", "Please fill in all fields.")
            return
        
        entry = Entry(date, title, content)
        self.entry_list.append(entry)
        self.save_entry_to_file(entry, font)
        
        # Clear the entry fields
        self.entry_text.delete("1.0", "end")
        
        # Set the title entry to display the placeholder text
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, "Enter Title")
        
        messagebox.showinfo("Success", "Entry added successfully!")
        
        # Update the Treeview with the latest entries
        self.populate_treeview_with_entries()
        
    def save_entry_to_file(self, entry, font):
        entry_filename = os.path.join(self.entries_folder, f"{entry.date}_{entry.title}.txt")
        with open(entry_filename, "w") as f:
            f.write(f"{entry.date}\n")
            f.write(f"{entry.title}\n")
            f.write(f"Font:{font}\n")
            f.write(f"Content:{entry.content}\n")
            
            
    def populate_treeview_with_entries(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        
        for filename in os.listdir(self.entries_folder):
            if filename.endswith(".txt"):
                with open(os.path.join(self.entries_folder, filename), "r") as f:
                    lines = f.readlines()
                    date = lines[0].replace("Date: ", "").strip()
                    title = lines[1].replace("Title: ", "").strip()
                    self.tree.insert("", "end", values=(date, title))
            
    def show_selected_entry(self, event):
        selected_item = self.tree.selection()[0]
        date, title = self.tree.item(selected_item, "values")
        
        entry_filename = os.path.join(self.entries_folder, f"{date}_{title}.txt")
        
        with open(entry_filename, "r") as f:
            lines = f.readlines()
            font = None
            content = []
            
            for line in lines:
                if line.startswith("Font:"):
                    font = line.replace("Font:", "").strip()
                elif line.startswith("Content:"):
                    content = line.split("Content:", 1)[-1].strip()


        # Open a new tab within the view_entry_notebook to show the selected entry
        self.view_entry_notebook.add(tk.Frame(self.view_entry_notebook), text=f"{title}")
        # Select the newly created tab
        self.view_entry_notebook.select(self.view_entry_notebook.tabs()[-1])
        # Display the selected entry in the new tab
        self.display_entry(title, date, content, font, entry_filename)
        ### GOT SOMEWHERE NOW NEED TO FIGURE OUT HOW TO DISPLAY THE ENTRY IN THE NEW TAB ### WITH THE EDIT AND DELETE BUTTONS
        
        
        
        ### OLD CODE FOR REFERENCE ###
        # entry_window = tk.Toplevel(self.root)
        # entry_window.title(f"{title} - {date}")
        
        # Change the icon of the window using the iconbitmap() method
        entry_window.iconbitmap(self.icon_path)
    
        
        entry_text = tk.Text(entry_window, height=20, width=60)
        entry_text.pack(padx=10, pady=10)
        
        entry_text.insert("end", content)
        entry_text.config(state="disabled", font=(font, 12))
        
        # Add an "Edit Entry" button that allows editing within the same window
        edit_entry_button = tk.Button(entry_window, text="Edit Entry", command=lambda: self.toggle_edit_entry(entry_text, content))
        edit_entry_button.pack(pady=5)
              
        # Add a "Delete Entry" button
        delete_button = tk.Button(entry_window, text="Delete Entry", command=lambda: self.confirm_delete(entry_filename))
        delete_button.pack(pady=5)
        
        
        # Drop down menu to select font   
        self.font_var.set(font)
        self.font_dropdown = tk.OptionMenu(entry_window, self.font_var, *self.list_of_fonts)
        self.font_dropdown.pack(pady=5)
        self.font_var.trace_add('write', lambda *args: self.change_font(entry_text, self.font_var.get()))
        # grey out the font selection dropdown
        self.font_dropdown.config(state="disabled")
        
        
         
        
    def toggle_edit_entry(self, entry_text, content):
        # undo the grey out of the font selection dropdown
        self.font_dropdown.config(state="normal")
        # Toggle the state of the text box for editing content
        current_state = entry_text.cget("state")
        new_state = "normal" if current_state == "disabled" else "disabled"
        entry_text.config(state=new_state)
        # Edit the text of the button to reflect the current state
        edit_entry_button = entry_text.master.children["!button"]
        edit_entry_button.config(text="Save Entry" if new_state == "normal" else "Edit Entry")
        # If the state is disabled, save the changes to disk
        if new_state == "disabled":
            # grey out the font selection dropdown now that the entry is saved
            self.font_dropdown.config(state="disabled")
            selected_item = self.tree.selection()[0]
            new_content = entry_text.get("1.0", "end-1c")
            self.save_changes(selected_item, new_content, entry_text)
        else:
            new_state = "normal"
            
            
              
        
    def save_changes(self, selected_item, new_content, entry_text):    
        # Get global reference to the entry_list
        global entry_list
        
        # Get the current content of the entry
        date, title = self.tree.item(selected_item, "values")
        entry_filename = os.path.join(self.entries_folder, f"{date}_{title}.txt")
        with open(entry_filename, "r") as f:
            content = f.read().split("Content:", 1)[-1]
             
        # If no changes were made, do nothing otherwise save the changes to disk
        if new_content == content:
            return
        else:
            # Overwrite the existing file with the new content
            date, title = self.tree.item(selected_item, "values")
            entry_filename = os.path.join(self.entries_folder, f"{date}_{title}.txt")
            with open(entry_filename, "w") as f:
                f.write(f"{date}\n")
                f.write(f"{title}\n")
                f.write(f"Font:{self.get_font()}\n")
                f.write(f"Content:{new_content}\n")
            
        
            # Refresh the Treeview to reflect changes
            self.populate_treeview_with_entries()
            
            messagebox.showinfo("Edit Entry", "Entry edited successfully!")
        
        
    def confirm_delete(self, entry_filename):
        # Prompt the user for a password to confirm deletion and set window size
        password = simpledialog.askstring("Delete Entry", "Enter password to confirm deletion:", parent=self.root, show="*")
        
        
        # Verify the entered password against a stored password
        stored_password = "boobs"  # Set your desired password here
        if password == stored_password:
            # If the password matches, delete the entry
            os.remove(entry_filename)
            messagebox.showinfo("Delete Entry", "Entry deleted successfully!")
            # Update the Treeview with the latest entries
            self.populate_treeview_with_entries()
            
        # else if cancel button is clicked, do nothing
        elif password is None:
            return
        
        else:
            messagebox.showerror("Delete Entry", "Incorrect password. Entry not deleted.")
        


# Run the app
if __name__ == "__main__":
    app = DiaryApp()
    
