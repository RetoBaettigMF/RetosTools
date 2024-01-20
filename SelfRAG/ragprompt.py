from gpt import getCompletion
from fileoperations import readfile

PROMPT = "Answer the following prompt based on the texts following the prompt. \n"\
"The texts are preceeded by a filename each. "\
"Include the filename in your answer in curly brackets. \n"\
"If you can't answer the question based on the texts, return 'I don't know'\n\n"\
"\nPrompt: {}"\
"\n\nTexts:\n {}"

def getTexts(texts):
    text = ""
    for entry in texts:
        filename = entry[0]
        text = text + "Filename: "+filename+"\n"+readfile(filename)+"\n\n"
    return text

def getAnswer(question, matches):
    text = getTexts(matches)
    prompt = PROMPT.format(question, text)
    print(prompt)
    answer = getCompletion(prompt)
    return answer
