from gpt import get_completion
from tools import Tools

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

def main():    
    tools = Tools()
    
    messages = [
        {"role": "system", "content": "You are a project management assistant and you answer questions about the time tracking data of the company."\
         "You can answer questions about the actual date and time and you can call SQL queries on the data. Show the data in tables if possible."}
    ]

    while True:
        user_input = input("You: ")
        if user_input == "":
            break
        messages.append({"role": "user", "content": user_input})
        reply = query_llm(messages, tools)
        print("AI: " + reply)
    

def chat():
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
    main()