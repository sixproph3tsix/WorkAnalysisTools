# Python Helper Code Snippet #8

import tkinter as tk
from tkinter import ttk
import time

def progress():
    progress_bar['maximum'] = 100
    for i in range(101):
        time.sleep(0.05)  # Simulate long-running task
        progress_bar['value'] = i
        root.update_idletasks()  # Update GUI

root = tk.Tk()
root.title("Progress Bar Example")

# Create Progressbar widget
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=300)
progress_bar.pack(pady=20)

# Create a button to start the progress
start_button = tk.Button(root, text='Start', command=progress)
start_button.pack(pady=10)

root.mainloop()