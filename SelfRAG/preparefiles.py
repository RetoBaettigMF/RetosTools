import os
from fileoperations import readfile, getFiles

def preparefiles(pathfrom, pathto, maxsize=4000, overlap=1000):
    files = getFiles(pathfrom)
    os.makedirs(pathto, exist_ok=True)
    for file in files:
        chunks = []
        text = readfile(file)
        while (len(text) > 0):
            chunk = text[:maxsize]
            text = text[maxsize-overlap:]
            chunks.append(chunk)
        
        for i in range(len(chunks)):
            number = str(i).zfill(4)+"-"
            with open(os.path.join(pathto, number+os.path.basename(file)), 'w') as tofile:
                tofile.write(chunks[i])

