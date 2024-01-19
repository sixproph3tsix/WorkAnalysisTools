# LEFT OFF SETTING UP MODE 4


import math
import tkinter as tk
import os
import subprocess
import sys
import time

from tkinter import ttk

def display_files(found_files, mode):
    
    original_files = list(found_files)
    
    def line_count(afpath):
        """
        Count the number of lines in the file at the given path.
    
        Parameters:
        fpath (str): The path to the file.
    
        Returns:
        int: The number of lines in the file, or 0 if the file is not a text file or does not exist.
        """
        # Check if the file exists and is a text file
        if not os.path.isfile(afpath) or not afpath.lower().endswith('.txt'):
            return 0
        try:
            with open(afpath, 'r') as file:
                lines = file.readlines()
                return len(lines)
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0
    
    def populate_tree(files):
        for file in files:
            file_name = os.path.basename(file)
            file_path = os.path.dirname(file)
            if mode == 4:
                line_count(file)
            else:
                file_size = round(os.path.getsize(file)/1000, 1)
                tree.insert("", tk.END, values=(file_name, file_path, file_size))    
    
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
    root.title("Search Results")
    
    # Tree things
    tree_frame = ttk.Frame(root)
    tree_frame.pack(expand=True, fill="both")
    
    tree = ttk.Treeview(tree_frame, columns=("FileName", "FileLocation", "FileSize"), show='headings', height=25)

    tree.heading("FileName", text="File Name", command=lambda: treeview_sort_column(tree, "FileName", False))
    tree.heading("FileLocation", text="File Location", command=lambda: treeview_sort_column(tree, "FileLocation", False))
    tree.heading("FileSize", text="Size (KB)", command=lambda: treeview_sort_column(tree, "FileSize", False))

    tree.column("FileName", width=250)
    tree.column("FileLocation", width=350)
    tree.column("FileSize", width=100)

    # Scrollbars
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    h_scroll.pack(side="bottom", fill="x")

    tree.pack(expand=True, fill="both")
    tree.configure(xscrollcommand=h_scroll.set)
    
    control_frame = ttk.Frame(root)
    control_frame.pack(fill="x")

    size_label = ttk.Label(control_frame, text="Trim Less Than (KB):")
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

    time.sleep(1)
    found_files = []    

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
                    found_files.append(os.path.join(root, file))
    else:
        for item in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, item)) and file_matches(item):
                found_files.append(os.path.join(directory, item))

    return found_files

def main():
    directory = input("Enter the directory to search: ")

    recurs = input("\nSearch recursively? 1 for Yes, 0 for No: \n\n")
    recursive = recurs.strip() == "1"

    mode = input("\nChoose a search mode (1-4): " + \
                   "\n1) File Name EXACT" + \
                   "\n2) File Name CONTAINS" + \
                   "\n3) File Data CONTAINS" + \
                   "\n4) AF Search\n\n")

    if mode in ['1', '2', '3']:
        str_file = input("\nEnter search criteria: ")
        search_type = 'exact' if mode == '1' else 'contains'
        found_files = find_files(directory, str_file, recursive, search_type)
    elif mode == '4':
        str_afnum = input("\nEnter an AF number: ")
        found_files = find_files(directory, str_afnum, recursive, 'af_number')
        print("\n\nSuccess! Displaying " + str(len(found_files)) +" results... ")
        display_files(found_files, mode)
        return
    else:
        print("Invalid choice")
        return

    print("\n\nSuccess! Displaying " + str(len(found_files)) +" results... ")
    
    time.sleep(2)
    
    display_files(found_files)

if __name__ == "__main__":
    main()
