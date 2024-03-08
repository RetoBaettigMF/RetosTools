from gpt import get_completion
from tools import Tools
from datetime import datetime

def query_llm(messages, tools):
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


def main():    
    tools = Tools()
    
    messages = [
        {"role": "system", "content": "You are a project management assistant and you answer questions about the time tracking data of the company."\
         "You can answer questions about the actual date and time and you can call SQL queries on the data. Show the data in tables if possible. The actual year is "+
        str(datetime.now().year)+"."}
    ]

    while True:
        user_input = get_multiline_input("You: ")
        if user_input == "":
            break
        messages.append({"role": "user", "content": user_input})
        reply = query_llm(messages, tools)
        print("\nYOU:" + user_input)
        print("AI: " + reply)
    
if __name__ == "__main__":
    main()