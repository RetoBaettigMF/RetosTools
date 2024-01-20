from vectors import getVector
from vectordb import trainVectorDB, saveVectorDB, loadVectorDB, getMatches
from ragprompt import getAnswer
from preparefiles import preparefiles
import pandas as pd

DBFILE = "./vectordb.json"
DATAPATH = "./data"
PREPAREDDATAPATH = "./prepareddata"

def createVectorDB():
    print("Preparing files...")
    preparefiles(DATAPATH, PREPAREDDATAPATH)
    print("Training vector database...")
    db = trainVectorDB(PREPAREDDATAPATH)
    print("Saving vector database...")
    saveVectorDB(DBFILE, db)
    return db

def getVectorDB():
    db=loadVectorDB(DBFILE)
    if len(db) == 0:
        print("No vector database found. Creating one...")
        db = createVectorDB()
    
    assert(len(db) > 0)
    return db


def main():
    # print(GPT("Write a funny sentence to welcome the user to the SelfRAG program."))
    print("Welcome to SelfRAG")
    
    db = getVectorDB()

    # read prompt from user
    while True:
        prompt = input("Enter a prompt: ")
        if prompt == "":
            break

        vector = getVector(prompt)
        matches = getMatches(db, vector)
        df = pd.DataFrame(matches, columns=['filename', 'score'])
        print(df)

        answer = getAnswer(prompt, matches)
        print(answer)


if __name__ == "__main__":
    main()