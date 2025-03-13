import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import glob
import json

# Define base paths for both games dynamically
appdata_roaming = os.getenv('APPDATA')
ds3_base_path = os.path.join(appdata_roaming, 'DarkSoulsIII')
elden_ring_base_path = os.path.join(appdata_roaming, 'EldenRing')
config_file = os.path.join(os.path.expanduser('~'), 'ds3_auto_save_config.json')

# Load configuration
def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('destination_dir', None)
    return None

# Save configuration
def save_config(destination_dir):
    with open(config_file, 'w') as f:
        json.dump({'destination_dir': destination_dir}, f)

# Initialize destination directory
destination_dir = load_config()

# Function to find the .sl2 file for the selected game
def find_sl2_file(base_path, game_name):
    search_pattern = os.path.join(base_path, '**', '*.sl2')
    sl2_files = glob.glob(search_pattern, recursive=True)
    if game_name == "Elden Ring":
        sl2_files = [f for f in sl2_files if not f.endswith('.sl2.bak')]
    return sl2_files[0] if sl2_files else None

# Function to get the selected game path
def get_game_path(game):
    if game == "Dark Souls 3":
        path = find_sl2_file(ds3_base_path, game)
        return path, os.path.join(destination_dir, 'Dark Souls III Save File')
    elif game == "Elden Ring":
        path = find_sl2_file(elden_ring_base_path, game)
        return path, os.path.join(destination_dir, 'Elden Ring Save File')
    else:
        return None, None

def copy_file():
    game = game_var.get()
    path, sub_dir = get_game_path(game)
    destination_file = os.path.join(sub_dir, os.path.basename(path))
    
    if path and os.path.exists(path):
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

def choose_destination():
    global destination_dir
    destination_dir = filedialog.askdirectory()
    if destination_dir:
        save_config(destination_dir)
        messagebox.showinfo("Success", f"Destination folder set to {destination_dir}")

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

# Check if destination directory is set, if not prompt the user
if not destination_dir:
    choose_destination()

# Run the application
root.mainloop()