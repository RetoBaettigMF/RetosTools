from gpt import GPT
from vectors import getVector
from vectordb import trainVectorDB, saveVectorDB, loadVectorDB
from preparefiles import preparefiles

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




    
    

if __name__ == "__main__":
    main()