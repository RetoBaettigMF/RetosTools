import os

def readfile(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def getFiles(path):
    files = []
    for file in os.listdir(path):
        files.append(os.path.join(path, file))
    return files

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

