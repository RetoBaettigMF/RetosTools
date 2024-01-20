from vectors import get_vector
from vectordb import getMatches
from ragprompt import get_answer
import pandas as pd
import re

def get_filename(answer):
    filename = re.search(r"\{(.+?)\}", answer)
    if filename:
        filename = filename.group(1)
        # remove the 4-digit index of the chung from the filename
        filename = re.sub(r'\d{4}-', '', filename)
    else:
        filename = ""
    return filename

def init_result(prompt, matches, answer):
    result = {
        "prompt": prompt,
        "matches": matches,
        "answer": answer
    }
    return result

def add_feedback(result):
    answer_improved = ""
    ok = input("Is this answer ok? (y/n): ")
    if ok == "":
        return None
    ok = (ok.upper() == "Y")
    if not ok:
        answer_improved = input("Enter the correct answer: ")

    result["ok"] = ok
    result["answer_improved"] = answer_improved
    return result
    
def execute_prompt(prompt, db, get_feedback=False, verbose=False):
    vector = get_vector(prompt)
    matches = getMatches(db, vector)
        
    answer = get_answer(prompt, matches)
    
    if verbose: 
        print("\nPrompt:",prompt)
        print("\nAnswer:",answer)
        print("\nMatches:")
        df = pd.DataFrame(matches, columns=['filename', 'score'])
        print(df)

    result = init_result(prompt, matches, answer)

    if get_feedback:
        result = add_feedback(result)

    return result

