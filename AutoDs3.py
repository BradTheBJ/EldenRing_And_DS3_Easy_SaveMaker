import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Define paths for both games
ds3_path = 'C:\\Users\\benjo\\AppData\\Roaming\\DarkSoulsIII\\01100001135b0a20\\ds30000.sl2'
elden_ring_path = 'C:\\Users\\benjo\\AppData\\Roaming\\EldenRing\\76561198284999200\\ER0000.sl2'
destination_dir = 'D:\\Temporary Souls Like Save Files'

# Function to get the selected game path
def get_game_path(game):
    if game == "Dark Souls 3":
        return ds3_path, os.path.join(destination_dir, 'Dark Souls III Save File')
    elif game == "Elden Ring":
        return elden_ring_path, os.path.join(destination_dir, 'Elden Ring Save File')
    else:
        return None, None

def copy_file():
    game = game_var.get()
    path, sub_dir = get_game_path(game)
    destination_file = os.path.join(sub_dir, os.path.basename(path))
    
    if os.path.exists(path):
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
        shutil.copyfile(path, destination_file)
        messagebox.showinfo("Success", f"File copied to {destination_file}")
    else:
        messagebox.showerror("Error", "File not found")

def delete_file():
    game = game_var.get()
    _, sub_dir = get_game_path(game)
    
    if os.path.exists(sub_dir):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this save file?"):
            shutil.rmtree(sub_dir)
            messagebox.showinfo("Success", "Save file deleted")
    else:
        messagebox.showerror("Error", "Folder not found")

def load_file():
    game = game_var.get()
    path, sub_dir = get_game_path(game)
    destination_file = os.path.join(sub_dir, os.path.basename(path))
    
    if os.path.exists(destination_file):
        shutil.copyfile(destination_file, path)
        messagebox.showinfo("Success", f"File loaded from {destination_file}")
    else:
        messagebox.showerror("Error", "Save file not found in the save file folder")

def select_game(event):
    copy_button.config(state=tk.NORMAL)
    delete_button.config(state=tk.NORMAL)
    load_button.config(state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("Save File Manager")
root.geometry("800x600")  # Set the window size

# Add a label for instructions
label = tk.Label(root, text="Select the game and choose an action:", font=("Helvetica", 16))
label.pack(pady=20)

# Create a dropdown menu to select the game
game_var = tk.StringVar(root)
game_menu = ttk.Combobox(root, textvariable=game_var, values=["Dark Souls 3", "Elden Ring"], font=("Helvetica", 14), state="readonly")
game_menu.set("Select Game")  # Default value
game_menu.bind("<<ComboboxSelected>>", select_game)
game_menu.pack(pady=20)

# Create and place the action buttons with styling
copy_button = tk.Button(root, text="Copy File", command=copy_file, width=30, height=3, bg="lightblue", font=("Helvetica", 14), state=tk.DISABLED)
copy_button.pack(pady=20)

delete_button = tk.Button(root, text="Delete Folder", command=delete_file, width=30, height=3, bg="lightcoral", font=("Helvetica", 14), state=tk.DISABLED)
delete_button.pack(pady=20)

load_button = tk.Button(root, text="Load File", command=load_file, width=30, height=3, bg="lightgreen", font=("Helvetica", 14), state=tk.DISABLED)
load_button.pack(pady=20)

# Run the application
root.mainloop()