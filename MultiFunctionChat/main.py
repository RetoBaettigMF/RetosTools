from gpt import get_completion
from tools import Tools
from datetime import datetime
from rolx import get_rolx_data

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
        {"role": "system", "content": "You are a helpful assistant and you try to execute the wishes of the user by using all your abilities."\
         "You can make multiple tool calls to support the user. Use the following functions \n"\
         "- get_now: to get current date and time\n"\
         "- execute_python_code: to execute programs\n"\
         "- get_timesheet_entries: to get timesheet and project data\n"            
         "- scrape: to scrape a website. Use it to get information from links you found via google_search\n"\
         "- google_search: to search google\n"\
         "If the user asks a question, make a plan to solve the problem and execute the plan."
        }
    ]

    while True:
        user_input = get_multiline_input("You: ")
        if user_input == "":
            if input("Wirklich beenden (y/n)?").lower() == "y":
                break
            else:
                continue
        messages.append({"role": "user", "content": user_input})
        reply = query_llm(messages, tools)
        print("\nYOU:" + user_input)
        print("AI: " + reply)
    
if __name__ == "__main__":
    main()