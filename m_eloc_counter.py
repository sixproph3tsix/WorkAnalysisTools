import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def show_message(location):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Message", "File saved at...  " + location)
    root.destroy()  # Destroy the window after displaying the message

def askDir():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()  # Destroy the window after use
    return path

def saveFile(df, location):
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

    show_message(location)
    root.destroy()
    if filename:  # Check if a filename was given
        df.to_excel(filename, index=False)

def elocCounter(filepath):
    loc = 0
    cloc = 0
    with open(filepath, 'r', encoding='utf-8') as file:  # Added encoding
        for line in file:
            loc += 1
            if line.startswith('%'):
                cloc += 1
    eloc = loc - cloc
    return loc, cloc, eloc

def searchDir(directory):
    data = {"File Name": [], "File Path": [], "Total LOC": [], "Comment LOC": [], "Executable LOC": []}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.m'):
                file_path = os.path.join(root, file)
                data["File Name"].append(file)
                data["File Path"].append(file_path)
                
                loc, cloc, eloc = elocCounter(file_path)
                
                data["Total LOC"].append(loc)
                data["Comment LOC"].append(cloc)
                data["Executable LOC"].append(eloc)
                
    return pd.DataFrame(data)

path = askDir()
df = searchDir(path)
saveFile(df, path)  # Pass the DataFrame to the function