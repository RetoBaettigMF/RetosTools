from vectors import getVector
from fileoperations import readfile, getFiles
import json
import os

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
        
