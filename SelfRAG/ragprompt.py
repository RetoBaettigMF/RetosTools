from gpt import get_completion
from fileoperations import read_file
from settings import RAG_PROMPT

def get_texts(texts):
    text = ""
    for entry in texts:
        filename = entry[0]
        text = text + "Filename: "+filename+"\n"+read_file(filename)+"\n\n"
    return text

def get_answer(question, matches):
    text = get_texts(matches)
    prompt = RAG_PROMPT.format(question, text)
    answer = get_completion(prompt)
    return answer
