import os
from fileoperations import read_file, get_files, delete_directory, write_file

def prepare_files(pathfrom, pathto, maxsize=4000, overlap=1000):
    files = get_files(pathfrom)
    delete_directory(pathto)
    os.makedirs(pathto, exist_ok=True)
    for file in files:
        chunks = []
        text = read_file(file)
        while (len(text) > 0):
            chunk = text[:maxsize]
            text = text[maxsize-overlap:]
            chunks.append(chunk)
        
        for i in range(len(chunks)):
            number = str(i).zfill(4)+"-"
            write_file(os.path.join(pathto, number+os.path.basename(file)), chunks[i])

