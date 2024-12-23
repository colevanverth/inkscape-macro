import time
from pynput import keyboard
import shutil
import sys
import subprocess
import os
import tempfile
from Foundation import NSData
from AppKit import NSPasteboardTypePNG, NSPasteboardTypeTIFF, NSPasteboard

TEMPLATE_FN = "Anki.svg"
RENDER_FN = "display.tex"
STORAGE_DIR = "files"
ACTION = '''--actions="export-filename:REPLACE.pdf; export-height:300; export-width: 650; export-dpi: 300; export-type:pdf; export-latex; export-do"'''

def handle_inkscape():
    filenum = len(os.listdir(STORAGE_DIR)) + 1
    fn = f"files/{filenum}.svg"
    shutil.copy(TEMPLATE_FN, fn)
    m_time = os.path.getmtime(fn)
    p = subprocess.Popen(["inkscape", fn])

    while True:
        time.sleep(0.25)
        if os.path.getmtime(fn) != m_time:
            m_time = os.path.getmtime(fn)
            export_pipeline(fn)
        elif p.poll() != None:
            return

def copy_to_clipboard(fn):
    format = "PNG" 
    pasteboard = NSPasteboard.generalPasteboard()
    image_data = NSData.dataWithContentsOfFile_(fn)
    format_type = NSPasteboardTypePNG
    pasteboard.clearContents()
    pasteboard.setData_forType_(image_data, format_type)

def export_pipeline(fn):
    temp_dir = tempfile.TemporaryDirectory()
    
    fn_base = fn.removeprefix("files/").removesuffix(".svg")

    # Export .svg on Inkscape.
    action = ACTION.replace("REPLACE", f"{temp_dir.name}/{fn_base}")
    subprocess.run(f"inkscape {action} {fn}", shell=True)

    # Setup .tex file for rendering.
    with open(RENDER_FN, "rt") as file:
        tex = file.read()
    tex = tex.replace("REPLACE", fn_base)
    with open(f"{temp_dir.name}/{fn_base}_render.tex", "wt") as file:
        file.write(tex)

    # Create .pdf then convert to .png and copy to clipboard.
    subprocess.run(f"pdflatex {fn_base}_render.tex", shell=True, cwd=temp_dir.name)
    subprocess.run(f"convert -density 300 -background transparent {fn_base}_render.pdf {fn_base}.png", shell=True, cwd=temp_dir.name)

    # Copy png to clipboard
    copy_to_clipboard(f"{temp_dir.name}/{fn_base}.png")
    temp_dir.cleanup()

def main():
    if not os.path.exists("files"):
        os.makedirs("files") 

    with keyboard.GlobalHotKeys({'<ctrl>+t': handle_inkscape}) as hotkey:
        hotkey.join()
    
if __name__ == "__main__":
    main()
