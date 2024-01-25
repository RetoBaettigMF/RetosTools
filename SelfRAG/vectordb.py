from vectors import get_nearest_neighbors
from gpt import get_vector
from fileoperations import read_file, get_files
from preparefiles import prepare_files
import json
from settings import DATA_PATH, PREPARED_DATA_PATH, DB_FILE

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
        
def create_vector_db():
    print("Preparing files...")
    prepare_files(DATA_PATH, PREPARED_DATA_PATH)
    print("Training vector database...")
    db = train_vector_db(PREPARED_DATA_PATH)
    print("Saving vector database...")
    save_vector_db(DB_FILE, db)
    return db

def get_vector_db():
    db=load_vector_db(DB_FILE)
    if len(db) == 0:
        print("No vector database found. Creating one...")
        db = create_vector_db()
    
    assert(len(db) > 0)
    return db