import os
from fileoperations import read_file, get_files, delete_directory, write_file, change_file_path, change_file_type
from convert_html import convert_html_to_md
from settings import TEXT_CHUNK_OVERLAP, TEXT_CHUNK_MAXSIZE
import fnmatch

def trimback(text, maxtrim=TEXT_CHUNK_OVERLAP/4):
    minpos = max(len(text)-maxtrim-1, 0)
    cutpos = len(text)-1
    while cutpos > minpos:
        if text[cutpos] == "\n":
            return text[:cutpos]
        cutpos -= 1
    
    return text

def trimfront(text, maxtrim=round(TEXT_CHUNK_OVERLAP/4)):
    maxpos = min(maxtrim, len(text))
    cutpos = 0
    while cutpos < maxpos:
        if text[cutpos] == " " or text[-maxpos] == "\n":
            return text[cutpos:]
        cutpos += 1
    
    return text

def is_html_file(filename):
    filename = filename.lower()
    return filename.endswith(".html") or filename.endswith(".htm") or filename.endswith(".xhtml") or filename.endswith(".xhtm") 

def file_already_converted(file, pathto):
    file_without_extension = os.path.splitext(file)[0]
    for root, dirs, files in os.walk(pathto):
        for file in files:
            if fnmatch.fnmatch(file, f"*{file_without_extension}*"):
                return True
    return False
    
    
def prepare_files(pathfrom, pathto, maxsize=TEXT_CHUNK_MAXSIZE, overlap=TEXT_CHUNK_OVERLAP):
    #delete_directory(pathto)
    os.makedirs(pathto, exist_ok=True)

    for root, dirs, files in os.walk(pathfrom):
        for file in files:
            if file_already_converted(file, pathto):
                print(f"File {file} already converted. Skipping.")
                continue
            file_path = os.path.join(root, file)
            print(file_path)
            chunks = []
            text = read_file(file_path)

            if is_html_file(file):
                text = convert_html_to_md(text)
                file_path = change_file_type(file_path, ".md")

            while len(text) > 0:
                chunk = trimback(text[:maxsize])
                text = trimfront(text[maxsize-overlap:])
                chunks.append(chunk)

            # Erstelle das entsprechende Ausgabeverzeichnis
            relative_path = os.path.relpath(root, pathfrom)
            output_dir = os.path.join(pathto, relative_path)
            os.makedirs(output_dir, exist_ok=True)

            for i in range(len(chunks)):
                number = str(i).zfill(4) + "-"
                output_file_path = os.path.join(output_dir, number + os.path.basename(file_path))
                write_file(output_file_path, chunks[i])