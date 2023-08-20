import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import datetime

class Entry:
    def __init__(self, date, title, content):
        self.date = date
        self.title = title
        self.content = content

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DearDiary")
        
        self.entry_list = []
        self.entries_folder = "diary_entries"
        
        # Create the entries folder if it doesn't exist
        os.makedirs(self.entries_folder, exist_ok=True)
        
        self.create_ui()
        
    
    def create_ui(self):
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=0, padx=10, pady=5)
        self.date_entry.config(bg="#fbf2c0")  # Set the background color here
        
        # Automatically set the current date in the date_entry field
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_entry.insert(0, current_date)
        
        self.title_entry = PlaceholderEntry(self.root, "Enter Title")
        self.title_entry.grid(row=1, column=0, padx=10, pady=5)
        self.title_entry.config(bg="#fbf2c0")  # Set the background color here
        
        self.entry_text = tk.Text(self.root, height=15, width=60) # Adjust height and width as needed
        self.entry_text.grid(row=2, column=0, padx=10, pady=10)
        self.entry_text.config(bg="#fbf2c0")  # Set the background color here
        
        add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry, width=20)
        add_button.grid(row=3, column=0, pady=5)
        
        self.tree = ttk.Treeview(self.root, columns=("Date", "Title"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Title", text="Title")
        
        # Configure the Treeview style to change the background color of the section
        style = ttk.Style()
        style.configure("Treeview", background="#fbf2c0")  # Set the desired background color
        
        
        self.tree.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")
        
        # Populate the treeview with existing entries
        self.populate_treeview_with_entries()
        
        # Bind double click to show selected entry
        self.tree.bind("<Double-1>", self.show_selected_entry)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        
        
    def add_entry(self):
        date = self.date_entry.get()
        title = self.title_entry.get()
        content = self.entry_text.get("1.0", "end-1c")
        
        # Automatically set the current date in the date_entry field
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, current_date)
        
        if title == "Enter Title" or not content:
            messagebox.showwarning("Incomplete Entry", "Please fill in all fields.")
            return
        
        entry = Entry(date, title, content)
        self.entry_list.append(entry)
        self.save_entry_to_file(entry)
        
        # Clear the entry fields
        self.entry_text.delete("1.0", "end")
        
        # Set the title entry to display the placeholder text
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, "Enter Title")
        
        messagebox.showinfo("Success", "Entry added successfully!")
        
        # Update the Treeview with the latest entries
        self.populate_treeview_with_entries()
        
    def save_entry_to_file(self, entry):
        entry_filename = os.path.join(self.entries_folder, f"{entry.date}_{entry.title}.txt")
        with open(entry_filename, "w") as f:
            f.write(f"{entry.date}\n")
            f.write(f"{entry.title}\n")
            f.write(f"Content:\n{entry.content}\n")
            
            
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
            content = f.read().split("Content:\n", 1)[-1]  # Extract only the content
        
        entry_window = tk.Toplevel(self.root)
        entry_window.title(f"{title} - {date}")
        
        # Set the icon for the view_entries window
        icon_path = "diary_pic.ico"  # Replace with the path to your icon file
        entry_window.iconbitmap(icon_path)
        
        # Set the background color of the entry_window
        entry_window.config(bg="#43281c")  # Set your desired background color
        
        entry_text = tk.Text(entry_window, height=20, width=60)
        entry_text.pack(padx=10, pady=10)
        
        # Set the background color of the text box where entry content is displayed
        entry_text.config(bg="#fbf2c0")  # Replace with your desired color
        
        entry_text.insert("end", content)
        entry_text.config(state="disabled")
        
        # Add an "Edit Entry" button that allows editing within the same window
        edit_entry_button = tk.Button(entry_window, text="Edit Entry", command=lambda: self.toggle_edit_entry(entry_text, content))
        edit_entry_button.pack(pady=5)
              
        # Add a "Delete Entry" button
        delete_button = tk.Button(entry_window, text="Delete Entry", command=lambda: self.confirm_delete(entry_filename))
        delete_button.pack(pady=5)
        
        
    def toggle_edit_entry(self, entry_text, content):
        # Toggle the state of the text box for editing content
        current_state = entry_text.cget("state")
        new_state = "normal" if current_state == "disabled" else "disabled"
        entry_text.config(state=new_state)
        # Edit the text of the button to reflect the current state
        edit_entry_button = entry_text.master.children["!button"]
        edit_entry_button.config(text="Save Entry" if new_state == "normal" else "Edit Entry")
        # If the state is disabled, save the changes to disk
        if new_state == "disabled":
            selected_item = self.tree.selection()[0]
            new_content = entry_text.get("1.0", "end-1c")
            self.save_changes(selected_item, new_content, entry_text)
              
        
    def save_changes(self, selected_item, new_content, entry_text):    
        # Get global reference to the entry_list
        global entry_list
        
        # Get the current content of the entry
        date, title = self.tree.item(selected_item, "values")
        entry_filename = os.path.join(self.entries_folder, f"{date}_{title}.txt")
        with open(entry_filename, "r") as f:
            content = f.read().split("Content:\n", 1)[-1]
             
        # If no changes were made, do nothing otherwise save the changes to disk
        if new_content == content:
            return
        else:
            # Overwrite the existing file with the new content
            date, title = self.tree.item(selected_item, "values")
            entry_filename = os.path.join(self.entries_folder, f"{date}_{title}.txt")
            with open(entry_filename, "w") as f:
                f.write(f"Date: {date}\n")
                f.write(f"Title: {title}\n")
                f.write(f"Content:\n{new_content}\n")
        
            # Refresh the Treeview to reflect changes
            self.populate_treeview_with_entries()
            
            messagebox.showinfo("Edit Entry", "Entry edited successfully!")
        
        
    def confirm_delete(self, entry_filename):
        # Prompt the user for a password to confirm deletion and set window size
        password = simpledialog.askstring("Delete Entry", "Enter password to confirm deletion:", parent=self.root, show="*")
        
        
        # Verify the entered password against a stored password
        stored_password = "notboobs"  # Set your desired password here
        if password == stored_password:
            # If the password matches, delete the entry
            os.remove(entry_filename)
            messagebox.showinfo("Delete Entry", "Entry deleted successfully!")
            # Update the Treeview with the latest entries
            self.populate_treeview_with_entries()
        else:
            messagebox.showerror("Delete Entry", "Incorrect password. Entry not deleted.")

         
class PlaceholderEntry(tk.Entry):
    def __init__(self, parent, placeholder, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.placeholder = placeholder
        self.default_fg_color = self['fg']
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.put_placeholder()

    def focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color

    def focus_out(self, event):
        if not self.get():
            self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = 'black'
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1080x560")  # Set the size of the main window
    
    # Change the background color of the root window
    root.configure(bg="#43281c")
    
    # Change the icon of the window using the iconbitmap() method
    icon_path = "diary_pic.ico"  # path to icon file
    root.iconbitmap(icon_path)
    
    app = DiaryApp(root)
    root.mainloop()
