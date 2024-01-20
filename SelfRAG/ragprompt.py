from gpt import get_completion
from fileoperations import read_file

PROMPT = "Answer the following prompt based on the texts following the prompt. \n"\
"The texts are preceeded by a filename each. "\
"Include the filename in your answer in curly brackets. \n"\
"If you can't answer the question based on the texts, return 'I don't know'\n\n"\
"\nPrompt: {}"\
"\n\nTexts:\n {}"

def get_texts(texts):
    text = ""
    for entry in texts:
        filename = entry[0]
        text = text + "Filename: "+filename+"\n"+read_file(filename)+"\n\n"
    return text

def get_answer(question, matches):
    text = get_texts(matches)
    prompt = PROMPT.format(question, text)
    answer = get_completion(prompt)
    return answer
