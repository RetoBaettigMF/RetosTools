from gpt import get_completion
from tools import Tools
from webserver import start_webserver
from settings import INITIAL_MESSAGE


messages = INITIAL_MESSAGE
tools = Tools()

def query_llm(messages, tools):
    try:
        completion = get_completion(messages=messages, tools=tools.get_tools())
        message = completion.choices[0].message
        messages.append(message) # extend conversation with assistant's reply

        tool_calls = message.tool_calls
        while tool_calls:
            for tool_call in tool_calls:
                tools.handle_tool_call(tool_call, messages)
            completion = get_completion(messages=messages, tools=tools.get_tools())
            message = completion.choices[0].message
            tool_calls = message.tool_calls
            messages.append(message) # extend conversation with assistant's reply
        return message.content
    except Exception as e:
        return str(e)

def get_multiline_input(prompt):
    inp = input(prompt)
    result = inp
    if inp.startswith("\"\"\""):
        while True:
            inp = input("")
            result+=inp
            if inp.endswith("\"\"\""):
                break
        
    return result

def get_answer(prompt):
    messages.append({"role": "user", "content": prompt})
    reply = query_llm(messages, tools)
    s = "AI: " + reply
    print(s)
    return s

def main():    
    global messages, initial_message
    
    
    while True:
        user_input = get_multiline_input("You: ")
        if user_input == "":
            if input("Wirklich beenden (y/n)?").lower() == "y":
                break
            else:
                continue
        get_answer(user_input)

    
if __name__ == "__main__":
    start_webserver(get_answer)
    main()