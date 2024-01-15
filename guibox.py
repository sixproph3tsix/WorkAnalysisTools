# Checks a specified directory for a specified file
# Returns the path to the specified file, as well as the file size
# Option to return the path to the specified file IF the file exceeds a specified size
# Option to return the path to the specified file IF the number of rows in the file are greater than 1 (is populated)
# Option to return the 

# Python Helper Code Snippet #5
import tkinter as tk
from tkinter import Listbox, Scrollbar, messagebox
import os
import subprocess
import sys

def open_selected_path():
    try:
        selected_index = listbox.curselection()[0]  # Get the index of the selected item
        selected_path = paths[selected_index]  # Get the path at that index

        # Open the path depending on the operating system
        if sys.platform == "win32":
            os.startfile(selected_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", selected_path])
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", selected_path])
    except IndexError:
        messagebox.showinfo("Info", "Please select a path from the list")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# List of paths to display (replace with your actual paths)
paths = [
    '/path/to/local/file_or_directory',
    '/path/to/another/file_or_directory',
    '\\\\network\\path\\to\\file_or_directory'  # Example network path for Windows
    # Add more paths as needed
]

# Set up the basic window
root = tk.Tk()
root.title("Path Selector")

# Create a Listbox widget
listbox = Listbox(root, width=50)
listbox.pack(padx=5, pady=10)

# Create a frame to contain the Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a vertical Scrollbar
v_scroll = Scrollbar(frame, orient="vertical")

# Create a Listbox widget with a specified width and set it to be scrollable
listbox = Listbox(frame, width=50, yscrollcommand=v_scroll.set)
listbox.pack(side="left", fill="y")

# Configure the Scrollbar
v_scroll.config(command=listbox.yview)
v_scroll.pack(side="right", fill="y")

# Add paths to the Listbox
for path in paths:
    listbox.insert(tk.END, path)

# Add a button that will trigger the opening of the selected path
open_button = tk.Button(root, text="Open Selected Path", command=open_selected_path)
open_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
