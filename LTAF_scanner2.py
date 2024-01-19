import tkinter as tk

def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Python GUI")

    # Create a text box
    text_box = tk.Entry(window, width=50)
    text_box.pack()

    # Create a dropdown menu
    options = [
        "option1",
        "option2",
        "option3",
        "option4"
    ]
    
    selected_option = tk.StringVar(window)
    selected_option.set(options[0])  # default value
    dropdown = tk.OptionMenu(window, selected_option, *options)
    dropdown.pack()

    # Start the GUI event loop
    window.mainloop()

# Call the function to create and display the GUI
create_gui()
