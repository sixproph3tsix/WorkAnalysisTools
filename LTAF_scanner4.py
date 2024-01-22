import math
import tkinter as tk
import os
import subprocess
import sys
import time
from tkinter import ttk

def display_files(found_files, mode):
    original_files = list(found_files)

    def remove_selected_lines():
        try:
            selected_items = tree.selection()  # Get the list of selected items
            for item in selected_items:
                tree.delete(item)  # Remove each selected item
        except Exception as e:
            print(f"Error removing selected lines: {e}")

    def populate_tree(files):
        for file in files:
            file_name = os.path.basename(file[0])
            file_path = os.path.dirname(file[0])
            file_size = round(os.path.getsize(file[0]) / 1000, 1)
            if mode == '1':
                file_lines = line_count(file[0])
            elif mode == '2':
                file_lines = file[1]  # Line number where the string was found

            tree.insert("", tk.END, values=(file_name, file_path, file_size, file_lines))

    def open_file(arg):
        try:
            selected_item = tree.focus()  # Get the selected item
            file_path = tree.item(selected_item)['values'][1]
            file_name = tree.item(selected_item)['values'][0]
            

            if arg == 1:
                selected = file_path = tree.item(selected_item)['values'][1]
            else:
                selected = os.path.join(file_path, file_name)  # Complete file path    

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
        col_index = tv["columns"].index(col)
        l = [(tv.item(k)["values"], k) for k in tv.get_children('')]
        if col == "FileSize" or col == "LineCount":
            l.sort(key=lambda t: int(math.floor(float(t[0][col_index]))), reverse=reverse)
        else:
            l.sort(key=lambda t: t[0][col_index], reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    root = tk.Tk()
    root.title("Search Results")

    tree_frame = ttk.Frame(root)
    tree_frame.pack(expand=True, fill="both")

    tree = ttk.Treeview(tree_frame, columns=("FileName", "FileLocation", "FileSize", "LineCount"), show='headings', height=25)
    tree.heading("FileName", text="File Name", command=lambda: treeview_sort_column(tree, "FileName", False))
    tree.heading("FileLocation", text="File Location", command=lambda: treeview_sort_column(tree, "FileLocation", False))
    tree.heading("FileSize", text="Size (KB)", command=lambda: treeview_sort_column(tree, "FileSize", False))
    tree.heading("LineCount", text="Line Count", command=lambda: treeview_sort_column(tree, "LineCount", False))

    tree.column("FileName", width=250)
    tree.column("FileLocation", width=350)
    tree.column("FileSize", width=100)
    tree.column("LineCount", width=100)

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

    remove_button = ttk.Button(control_frame, text="Remove Selected", command=remove_selected_lines)
    remove_button.pack(side="left", padx=10, pady=10)

    populate_tree(found_files)

    root.mainloop()
    
def start_over():
    print('Invalid choice. Restarting...\n\n')
    main()
    
def string_in_file(filepath, searchstr):
    try:
        with open(filepath, 'r') as file:
            for line_number, line in enumerate(file, 1):
                if searchstr in line:
                    return line_number
        return "NA"
    except FileNotFoundError:
        return 0

def line_count(afpath):
    if not os.path.isfile(afpath) or not afpath.lower().endswith('.txt'):
        return 0
    try:
        with open(afpath, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
    
def find_files(directory, search_str, recursive, mode):

    found_files = []
    line_num = 'NA'
    time.sleep(1)

    if mode == '2':
        scan_str = input("\nScanning for:  ")

    def match(filename):
        if mode == '1':
            return filename.startswith(f'AF{search_str}')
        elif mode == '2':
            return filename.startswith(f'logger_tac_{search_str}')
        else:
            start_over()



    if recursive:
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                filesplit = os.path.splitext(file)
                filename = filesplit[0]

                if match(filename):
                    fullpath = os.path.join(root, file)

                    if mode == '2':
                        line_num = string_in_file(fullpath, scan_str)
                        if line_num != "NA":
                            found_files.append((fullpath, line_num))
                    else:
                        found_files.append((fullpath, line_num))

    else:
        for file in os.listdir(directory):
            filesplit = os.path.splitext(file)
            filename = filesplit[0]
            
            if match(filename):
                print('test')
                fullpath = os.path.join(directory, file)
                
                if mode == '2':
                    line_num = string_in_file(fullpath, scan_str)
                    if line_num != "NA":
                        found_files.append((fullpath, line_num))
                else:
                    found_files.append((fullpath, line_num))

    return found_files

def main():
    directory = input("Enter the directory to search: ")

    if not os.path.isdir(directory):
        start_over()

    recurs = input("\nSearch recursive? \n0) No\n1) Yes\n")
    if recurs not in ['0', '1']:
        start_over()
    recursive = recurs.strip() == "1"

    mode = input("\nSearch mode:" + \
                 "\n1) AF Search" + \
                 "\n2) LT Search\n")

    if mode == '1':
        str_file = input("\nAF Number:  ")
    elif mode == '2':
        str_file = input("\nLT Number:  ")
    else:
        start_over()
    
    found_files = find_files(directory, str_file, recursive, mode)
    print("\n\nFinished. Displaying " + str(len(found_files)) + " results... ")
    time.sleep(2) # pause for legibility
    display_files(found_files, mode)

if __name__ == "__main__":
    main()