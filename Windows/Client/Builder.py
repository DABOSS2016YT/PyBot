# -*- coding: latin-1 -*-
import subprocess
import shutil
import sys
import time
import tkinter as tk
from tkinter import font

# Create a main window with specific resolution and placement
root = tk.Tk()
root.geometry("400x400")
root.title("GUI")
root.configure(bg='#2B2B2B')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Position the window in the center of the screen
root.update_idletasks()  # Ensure the window is properly sized before positioning
x = (screen_width // 2) - (root.winfo_width() // 2)
y = (screen_height // 2) - (root.winfo_height() // 2)
root.geometry(f'{root.winfo_width()}x{root.winfo_height()}+{x}+{y}')

root.resizable(False, False)

# Remove the window manager buttons (minimize, maximize, and close)
root.overrideredirect(True)

# Create a close button
def close_window():
    root.destroy()
    sys.exit()

close_button = tk.Button(root, text="\u2715", bg='#FF0000', fg='white', relief='flat', borderwidth=0, command=close_window, font=('Helvetica', 12), activeforeground='white', activebackground='#8B0000')
close_button.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-5, y=5, width=25, height=25)

# Create a label for the IP
ip_label = tk.Label(root, text="Enter the new IP address:", bg='#2B2B2B', font=('Helvetica', 12), fg='#E0E0E0')
ip_label.pack(pady=20)

# Create an entry for the IP
ip_entry = tk.Entry(root, width=50, relief='solid', borderwidth=2, bg='#2B2B2B', fg='#E0E0E0')
ip_entry.pack()

# Install requirements
def install_requirements():
    # Create a label for the status
    status_label = tk.Label(root, text="\u2026", bg='#2B2B2B', font=('Helvetica', 10), fg='darkgreen')
    status_label.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-10, y=-10, width=20, height=20)

    # Install the requirements
    try:
        subprocess.call(['pip', 'install', 'pyobf2'])
        install_status_label.config(text="Requirements installed.")
    except:
        install_status_label.config(text="Requirements failed to install")

    # Remove the status label
    status_label.destroy()


# Create a label for the install status
install_status_label = tk.Label(root, text="", bg='#2B2B2B', font=('Helvetica', 10), fg='darkgreen')
install_status_label.place(relx=0.5, rely=1.0, anchor=tk.S, x=-100, y=-20, width=200, height=20)

install_requirements()

# Create a build button
def build_file():
    # Create a copy of the original file
    shutil.copyfile('Client2.0.py', 'built.py')

    # Get the new value for server_ip
    new_server_ip = ip_entry.get()

    # Modify the new file
    with open('built.py', 'r') as f:
        lines = f.readlines()

    # Modify the server_ip variable
    lines[15] = 'server_ip = "' + new_server_ip +'"' '\n'

    # Write the modified file
    with open('built.py', 'w') as f:
        f.writelines(lines)

    # Display the success message
    success_label = tk.Label(root, text='File has been built.', bg='#2B2B2B', font=('Helvetica', 10), fg='#00FF00')
    success_label.pack()

build_button = tk.Button(root, text="Build", command=build_file, relief='solid', borderwidth=2, bg='#2B2B2B', fg='#E0E0E0', font=('Helvetica', 12))
build_button.pack(pady=20)

# Create an obfuscate button
def obfuscate_file():
    import pyobf2
    # Build the command to run Pyobfuscate
    command = ['pyobf2','built.py',]

    # Run the command
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Display the success message
    success_label = tk.Label(root, text='File has been obfuscated and saved as built.pyc.', bg='#2B2B2B', font=('Helvetica', 10), fg='#00FF00')
    success_label.pack()

obfuscate_button = tk.Button(root, text="Obfuscate", command=obfuscate_file, relief='solid', borderwidth=2, bg='#2B2B2B', fg='#E0E0E0', font=('Helvetica', 12))
obfuscate_button.pack(pady=20)

# Enter the main event loop
root.mainloop()