from vectors import get_vector
from vectordb import train_vector_db, save_vector_db, load_vector_db, getMatches
from ragprompt import get_answer
from preparefiles import prepare_files
from history import history
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

def get_feedback(prompt, matches, answer):
    answer_improved = ""
    ok = input("Is this answer ok? (y/n): ")
    if ok == "":
        return None
    ok = (ok.upper() == "Y")
    if not ok:
        answer_improved = input("Enter the correct answer: ")
        ok = "N"

    feedback = {
        "prompt": prompt,
        "matches": matches,
        "answer": answer,
        "ok": ok,
        "answer_improved": answer_improved
    }
    return feedback
    
def main():
    # print(GPT("Write a funny sentence to welcome the user to the SelfRAG program."))
    print("Welcome to SelfRAG")
    rag_history = history("history.json")
    
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

        feedback = get_feedback(prompt, matches, answer)
        rag_history.add(feedback)
        rag_history.save()
    
    
        



if __name__ == "__main__":
    main()