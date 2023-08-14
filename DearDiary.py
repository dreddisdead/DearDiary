import tkinter as tk
from tkinter import messagebox
import os

class Entry:
    def __init__(self, date, title, content):
        self.date = date
        self.title = title
        self.content = content

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary")
        
        self.entry_list = []
        self.entries_folder = "diary_entries"
        
        # Create the entries folder if it doesn't exist
        os.makedirs(self.entries_folder, exist_ok=True)
        
        self.create_ui()
    
    def create_ui(self):
        self.date_entry = PlaceholderEntry(self.root, "YYYY-MM-DD")
        self.date_entry.pack(padx=10, pady=5)
        
        self.title_entry = PlaceholderEntry(self.root, "Enter Title")
        self.title_entry.pack(padx=10, pady=5)
        
        self.entry_text = tk.Text(self.root, height=10, width=40)
        self.entry_text.pack(padx=10, pady=10)
        
        add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        add_button.pack(pady=5)
        
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
            f.write(f"Date: {entry.date}\n")
            f.write(f"Title: {entry.title}\n")
            f.write(f"Content:\n{entry.content}\n")
    
    def view_entries(self):
        if self.entry_list:
            entry_window = tk.Toplevel(self.root)
            entry_window.title("View Entries")
            
            entries_text = tk.Text(entry_window, height=10, width=40)
            entries_text.pack(padx=10, pady=10)
            
            for entry in self.entry_list:
                entries_text.insert("end", f"{entry.title}\n{entry.date}\n{entry.content}\n\n")
            
            entries_text.config(state="disabled")
        else:
            messagebox.showinfo("No Entries", "No entries to display.")
            
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
    app = DiaryApp(root)
    root.mainloop()
