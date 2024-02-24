from gpt import get_completion, get_single_completion
from readexcel import ExcelData
from fillword import WordFiller

messages = []

def chat():
    e = ExcelData()
    w = WordFiller(e)
    w.fill_words()
    messages = []
    while True:
        user_input = input("You: ")
        if user_input == "":
            break
        messages.append({"role": "user", "content": user_input})
        completion = get_completion(messages=messages)
        message=completion.choices[0].message
        messages.append(message)
        print("AI: " + message.content)


if __name__ == "__main__":
    chat()