from vectors import get_vector
from vectordb import train_vector_db, save_vector_db, load_vector_db, getMatches
from ragprompt import get_answer
from preparefiles import prepare_files
import pandas as pd

DB_FILE = "./vectordb.json"
DATA_PATH = "./data"
PREPARED_DATA_PATH = "./prepareddata"

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


def main():
    # print(GPT("Write a funny sentence to welcome the user to the SelfRAG program."))
    print("Welcome to SelfRAG")
    
    db = get_vector_db()

    # read prompt from user
    while True:
        prompt = input("Enter a prompt: ")
        if prompt == "":
            break

        vector = get_vector(prompt)
        matches = getMatches(db, vector)
        df = pd.DataFrame(matches, columns=['filename', 'score'])
        print(df)

        answer = get_answer(prompt, matches)
        print(answer)


if __name__ == "__main__":
    main()