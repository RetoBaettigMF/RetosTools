from vectordb import get_vector_db
from history import history
from rag import execute_prompt, get_filename
from settings import ANSWER_DONT_KNOW, HISTORY_FILE, REPLAY_HISTORY_FILE
from gpt import get_completion

def dont_know(answer):
    ansup = answer.upper()
    search = ANSWER_DONT_KNOW.upper()
    if (ansup.find(search) >= 0):
        return True
    return False

def ai_results_match(result_text, orig_result_text):
    prompt = "You are a quality assurance engineer and you have to decide if two texts roughly match in context not. \n"\
    "return only the word 'yes' or 'no' \n\n"\
    "Text1:\n {}"\
    "\n\nText2:\n {}"

    prompt = prompt.format(orig_result_text, result_text)

    result = get_completion(prompt)
    result = result.strip().upper()
    return (result == "YES")
    
def judge_result(result, orig_result):
    
    # Assumption: if the original reply was correct and the filename is the same in the original result and the replay result,
    # we assume the replay result is correct as well.
    # This assumption is not always correct, but it is correct often enough to be useful.
    filename1 = get_filename(result["answer"])
    filename2 = get_filename(orig_result["answer"])
    if (filename1 == filename2) and orig_result["ok"]:
        result["ok"] = True
        return result
    
    if dont_know(result["answer"]) and dont_know(orig_result["answer"]):
        result["ok"] = orig_result["ok"]
        return result
    
    if (dont_know(orig_result["answer"]) ^ dont_know(orig_result["answer"])) and orig_result["ok"]:
        result["ok"] = False
        return result
    
    if ai_results_match(result["answer"], orig_result["answer"]):
        result["ok"] = orig_result["ok"]
        return result
    
    print("\nprompt: ", result["prompt"])
    print("\norig answer: ", orig_result["answer"])
    print("\norig answer was correct: ", orig_result["ok"])
    print("\nreplay answer: ", result["answer"])
    ans = input("\nIs the replay answer correct? (y/n): ")
    ans = ans.upper()
    result["ok"] = (ans == "Y")
    return result
  
def main():
    # print(GPT("Write a funny sentence to welcome the user to the SelfRAG program."))
    print("Welcome to SelfRAG replay")
    rag_history = history(HISTORY_FILE)
    rag_history.print_statistics()
    replay_history = history(REPLAY_HISTORY_FILE)
    replay_history.clear()
    
    db = get_vector_db()

    # read prompt from user
    for orig_result in rag_history.get():
        prompt = orig_result["prompt"]
        result = execute_prompt(prompt, db, get_feedback=False)
        result = judge_result(result, orig_result)
        print("prompt: ", prompt)
        print("   before: ", orig_result["ok"], " after: ", result["ok"]);
        replay_history.add(result)
    
    replay_history.save()
    print("Original statistics:")
    rag_history.print_statistics()
    print("Replay statistics:")
    replay_history.print_statistics()
    print("Goodbye!")      
    
if __name__ == "__main__":
    main()