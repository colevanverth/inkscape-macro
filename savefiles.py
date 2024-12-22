import subprocess
import os
import time
 
STORAGE_DIR = "files"
TEX_FILE = "display.tex"
ACTION = '''--actions="export-filename:REPLACE.pdf; export-height:300; export-width: 650; export-dpi: 300; export-type:pdf; export-latex; export-do"'''

def process_file(filename):
    fn_base = filename.removesuffix(".svg") # files/example
    fn_stripped = fn_base.removeprefix("files/") # example
    fn_tex = fn_stripped + "_render.tex" # example_render.tex
    fn_tex_f = fn_base + "_render.tex" # files/example_render.tex
    fn_pdf = fn_base + ".pdf" # files/example.pdf
    fn_png = fn_base + ".png" # files/example.png

    # Export the files.
    action = ACTION.replace("REPLACE", fn_base)
    subprocess.run(f"inkscape {action} {filename}", shell=True)

    # Setup tex file.
    with open(TEX_FILE, "rt") as file:
        tex = file.read()
    tex = tex.replace("REPLACE", fn_stripped)
    with open(fn_tex_f, "wt") as file:
        file.write(tex)

    # Load the text file and convert to image.
    subprocess.run(f"pdflatex {fn_tex}", shell=True, cwd="files")
    subprocess.run(f"convert -density 300 -background transparent {fn_pdf} {fn_png}", shell=True)
  
def main():
    file_to_mtime = { f"{STORAGE_DIR}/{file}": os.path.getmtime(f"{STORAGE_DIR}/{file}") for file in os.listdir(STORAGE_DIR) }
    while True:
        time.sleep(0.25)
        for file in file_to_mtime.keys():
            if os.path.getmtime(file) != file_to_mtime[file]:
                process_file(file)
                file_to_mtime[file] = os.path.getmtime(file)



if __name__ == "__main__":
    main()
