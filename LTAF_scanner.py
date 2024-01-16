# Python Helper Code Snippet #12
import math
import tkinter as tk
import os
import subprocess
import sys
import time

from tkinter import ttk

def display_files(found_files):
    
    original_files = list(found_files)
    
    def populate_tree(files):
        for file in files:
            file_name = os.path.basename(file)
            file_size = round(os.path.getsize(file)/1000, 1)
            tree.insert("", tk.END, values=(file_name, file, file_size))    
    
    def open_file(arg):
        try:
            selected_item = tree.focus()  # Get the selected item
            selected = tree.item(selected_item)['values'][1]  # Get the file path from the second column
            if arg == 1:
                selected = os.path.dirname(selected)
            if sys.platform == "win32":
                os.startfile(selected)
            elif sys.platform == "darwin":
                subprocess.run(["open", selected])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", selected])
        except Exception as e:
            print(f"Error opening file: {e}")

    def trim_files():
        min_size = int(size_entry.get())
        for item in tree.get_children():
            if int(math.floor(float(tree.item(item)['values'][2]))) < min_size:
                tree.delete(item)

    def reset_list():
        tree.delete(*tree.get_children())  # Clear the tree view
        populate_tree(original_files)  # Repopulate with the original list

    def close_window():
        root.destroy()

    def treeview_sort_column(tv, col, reverse):
        
        # Determine the index of the column based on its heading
        col_index = tv["columns"].index(col)
        
        # Retrieve the data from the treeview as a list
        l = [(tv.item(k)["values"], k) for k in tv.get_children('')]
        
        # Check if we're sorting the File Size column and handle it as integers
        if col == "FileSize":
            l.sort(key=lambda t: int(math.floor(float(t[0][col_index]))), reverse=reverse)
        else:
            l.sort(key=lambda t: t[0][col_index], reverse=reverse)
    
        # Rearrange the items in the treeview according to the sorted list
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
    
        # Reverse the sort order for the next time the column is clicked
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    root = tk.Tk()
    root.title("File Search Results")
    
    # Tree things
    tree_frame = ttk.Frame(root)
    tree_frame.pack(expand=True, fill="both")
    
    tree = ttk.Treeview(tree_frame, columns=("FileName", "FilePath", "FileSize"), show='headings', height=25)

    tree.heading("FileName", text="File Name", command=lambda: treeview_sort_column(tree, "FileName", False))
    tree.heading("FilePath", text="File Path", command=lambda: treeview_sort_column(tree, "FilePath", False))
    tree.heading("FileSize", text="Size (KB)", command=lambda: treeview_sort_column(tree, "FileSize", False))

    tree.column("FileName", width=250)
    tree.column("FilePath", width=550)
    tree.column("FileSize", width=75)

    # Scrollbars
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    h_scroll.pack(side="bottom", fill="x")

    tree.pack(expand=True, fill="both")
    tree.configure(xscrollcommand=h_scroll.set)
    
    control_frame = ttk.Frame(root)
    control_frame.pack(fill="x")

    size_label = ttk.Label(control_frame, text="Trim File Size (KB):")
    size_label.pack(side="left", padx=10, pady=10)

    size_entry = ttk.Entry(control_frame)
    size_entry.pack(side="left", padx=10, pady=10)

    trim_button = ttk.Button(control_frame, text="Trim", command=trim_files)
    trim_button.pack(side="left", padx=10, pady=10)

    reset_button = ttk.Button(control_frame, text="Reset", command=reset_list)
    reset_button.pack(side="left", padx=10, pady=10)

    close_button = ttk.Button(control_frame, text="Close", command=close_window)
    close_button.pack(side="right", padx=20, pady=10)

    open_dirbutton = ttk.Button(control_frame, text="Open Location", command=lambda: open_file(1))
    open_dirbutton.pack(side="right", padx=10, pady=10)

    open_filebutton = ttk.Button(control_frame, text="Open File", command=lambda: open_file(0))
    open_filebutton.pack(side="right", padx=10, pady=10)

    # Initially populate the tree
    populate_tree(found_files)

    root.mainloop()

def find_files(directory, search_term, recursive, search_type):
    matching_files = []

    def file_matches(filename):
        if search_type == 'exact':
            return filename == search_term
        elif search_type == 'contains':
            return search_term in filename
        elif search_type == 'af_number':
            return filename.startswith(f'AF{search_term}')
        else:
            return False

    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file_matches(file):
                    matching_files.append(os.path.join(root, file))
    else:
        for item in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, item)) and file_matches(item):
                matching_files.append(os.path.join(directory, item))

    return matching_files

def check_multiline(fpath):
    """
    Check if the file at the given path is a text file and has more than one line.

    Parameters:
    fpath (str): The path to the file.

    Returns:
    bool: True if the file is a text file and has more than one line, False otherwise.
    """
    # Check if the file exists and is a text file
    if not os.path.isfile(fpath) or not fpath.lower().endswith('.txt'):
        return False

    try:
        with open(fpath, 'r') as file:
            lines = file.readlines()
            return len(lines) > 1
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def main():
    directory = input("Enter the directory to search: ")

    recurs = input("\nSearch recursively? 1 for Yes, 0 for No: \n\n")
    recursive = recurs.strip() == "1"

    choice = input("\nChoose an option (1-3):\n1) EXACT String Search\n2) CONTAINS String Search\n3) AF Number Search\n\n")

    if choice in ['1', '2']:
        str_file = input("\nEnter the search string: ")
        search_type = 'exact' if choice == '1' else 'contains'
        time.sleep(1)
        print("\n\nSearching......")
        found_files = find_files(directory, str_file, recursive, search_type)
    elif choice == '3':
        str_afnum = input("Enter the AF number: ")
        time.sleep(1)
        print("\n\nSearching...... ")
        found_files = find_files(directory, str_afnum, recursive, 'af_number')
    else:
        print("Invalid choice")
        return

    print("\n\nSuccess! Displaying " + str(len(found_files)) +" results... ")
    
    time.sleep(2)
    
    display_files(found_files)

if __name__ == "__main__":
    main()
