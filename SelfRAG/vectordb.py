from vectors import getVector
import json
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

def trainVectorDB(path):
    files = getFiles(path)
    vectors = []
    for index, file in enumerate(files):
        text = readfile(file)
        vector = getVector(text)
        vectors.append([vector, file])
        progress="{:.1f}".format(index/len(files)*100)
        print("Trained "+progress+"% of the vector database.", end="\r")
    print()
    return vectors

def saveVectorDB(filename, vectors):
    with open(filename, 'w') as file:
        json.dump(vectors, file)

def loadVectorDB(filename):
    try:
        with open(filename, 'r') as file:
            vectors = json.load(file)  
    except FileNotFoundError:
        vectors = []
    return vectors
        
