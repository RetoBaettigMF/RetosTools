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
    for file in files:
        text = readfile(file)
        vector = getVector(text)
        print(file, ":", vector)
        vectors.append([vector, file])
    return vectors

def saveVectorDB(filename, vectors):
    with open(filename, 'w') as file:
        json.dump(vectors, file)

def loadVectorDB(filename):
    with open(filename, 'r') as file:
        vectors = json.load(file)
    return vectors
        
