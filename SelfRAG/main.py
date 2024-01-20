from vectordb import get_vector_db
from history import history
from rag import execute_prompt
from settings import HISTORY_FILE
  
def main():
    # print(GPT("Write a funny sentence to welcome the user to the SelfRAG program."))
    print("Welcome to SelfRAG")
    rag_history = history(HISTORY_FILE)
    rag_history.print_statistics()
    
    db = get_vector_db()

    # read prompt from user
    while True:
        prompt = input("Enter a prompt: ")
        if prompt == "":
            break

        result = execute_prompt(prompt, db, get_feedback=True, verbose=True)
        rag_history.add(result)
        rag_history.save()
        rag_history.print_statistics()
    
    print("Goodbye!")      

if __name__ == "__main__":
    main()