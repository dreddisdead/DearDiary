import tkinter as tk
from tkinter import ttk, messagebox
import os

class Entry:
    def __init__(self, date, title, content):
        self.date = date
        self.title = title
        self.content = content

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dear Diary")
        
        self.entry_list = []
        self.entries_folder = "diary_entries"
        
        # Create the entries folder if it doesn't exist
        os.makedirs(self.entries_folder, exist_ok=True)
        
        self.create_ui()
    
    def create_ui(self):
        self.date_entry = PlaceholderEntry(self.root, "YYYY-MM-DD")
        self.date_entry.grid(row=0, column=0, padx=10, pady=5)
        
        self.title_entry = PlaceholderEntry(self.root, "Enter Title")
        self.title_entry.grid(row=1, column=0, padx=10, pady=5)
        
        self.entry_text = tk.Text(self.root, height=10, width=40)
        self.entry_text.grid(row=2, column=0, padx=10, pady=10)
        
        add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        add_button.grid(row=3, column=0, pady=5)
        
        self.tree = ttk.Treeview(self.root, columns=("Date", "Title"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Title", text="Title")
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
        
        if date == "YYYY-MM-DD" or title == "Enter Title" or not content:
            messagebox.showwarning("Incomplete Entry", "Please fill in all fields.")
            return
        
        entry = Entry(date, title, content)
        self.entry_list.append(entry)
        self.save_entry_to_file(entry)
        
        self.date_entry.delete(0, "end")
        self.title_entry.delete(0, "end")
        self.entry_text.delete("1.0", "end")
        
        messagebox.showinfo("Success", "Entry added successfully!")
        
    def save_entry_to_file(self, entry):
        entry_filename = os.path.join(self.entries_folder, f"{entry.date}_{entry.title}.txt")
        with open(entry_filename, "w") as f:
            f.write(f"{entry.date}\n")
            f.write(f"{entry.title}\n")
            f.write(f"{entry.content}\n")
            
            
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
            content = f.read()
        
        entry_window = tk.Toplevel(self.root)
        entry_window.title(f"{title}")
        
        entry_text = tk.Text(entry_window, height=10, width=40)
        entry_text.pack(padx=10, pady=10)
        
        entry_text.insert("end", content)
        entry_text.config(state="disabled")
            
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
        self['fg'] = 'grey'
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")  # Set the size of the main window
    app = DiaryApp(root)
    root.mainloop()
