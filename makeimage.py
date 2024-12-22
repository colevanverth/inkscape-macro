from pynput import keyboard
import shutil
import subprocess
import os

STORAGE_DIR = "files"

def on_trigger():
    filenum = len(os.listdir(STORAGE_DIR)) + 1
    filename = f"files/{filenum}.svg"
    shutil.copy("Anki.svg", filename)
    subprocess.Popen(["inkscape", filename])

def main():
    with keyboard.GlobalHotKeys({'<ctrl>+t': on_trigger}) as hotkey:
        hotkey.join()

if __name__ == "__main__":
    main()
