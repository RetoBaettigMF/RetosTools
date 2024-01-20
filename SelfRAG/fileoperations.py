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