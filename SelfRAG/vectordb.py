from vectors import get_vector, get_nearest_neighbors
from fileoperations import read_file, get_files
import json
import os

def train_vector_db(path):
    files = get_files(path)
    vectors = []
    for index, file in enumerate(files):
        text = read_file(file)
        vector = get_vector(text)
        vectors.append([vector, file])
        progress="{:.1f}".format(index/len(files)*100)
        print("Trained "+progress+"% of the vector database.", end="\r")
    print()
    return vectors

def save_vector_db(filename, vectors):
    with open(filename, 'w') as file:
        json.dump(vectors, file)

def load_vector_db(filename):
    try:
        with open(filename, 'r') as file:
            vectors = json.load(file)  
    except FileNotFoundError:
        vectors = []
    return vectors


def getMatches(db, vector):
    result = []
    vectors = [row[0] for row in db]
    neighbors = get_nearest_neighbors(vector, vectors, 5)
    for neighbor in neighbors:
        result.append((db[neighbor[1]][1], neighbor[0]))
    return result
        
