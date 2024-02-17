from gpt import get_completion, get_single_completion
import pandas as pd
from pandasql import sqldf
import datetime
import json

data = pd.read_excel("rolx-export.xlsx")

def get_data(sql_query):
    try:
        result = sqldf(sql_query, globals())
    except Exception as e:
        return json.dumps({"error": str(e)})
    
    result = result.to_json(orient="records")
    return result

def get_now():
    # Erhalte das aktuelle Datum und die aktuelle Zeit
    now = datetime.datetime.now()

    # Konvertiere das Datum und die Zeit in einen String
    str = now.strftime("%d.%m.%Y %H:%M:%S")
    return json.dumps({"datetime": str})

def handle_tool_call(tool_call, messages):
    if not tool_call:
        return None
    
    available_functions = {
        "get_now": get_now,
        "get_data": get_data
    }  # only one function in this example, but you can have multiple
    # Step 4: send the info for each function call and function response to the model
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)

    print("Calling function: ", function_name, " with args: ", function_args)

    if function_name == "get_now":
        function_response = function_to_call()
    elif function_name == "get_data":
        function_response = function_to_call(
            sql_query=function_args.get("query")
        )

    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response
        }
    )  # extend conversation with function response

def query_llm(messages, tools):
    completion = get_completion(messages=messages, tools=tools)
    message = completion.choices[0].message
    messages.append(message) # extend conversation with assistant's reply

    tool_calls = message.tool_calls
    while tool_calls:
        for tool_call in tool_calls:
            handle_tool_call(tool_call, messages)
        completion = get_completion(messages=messages, tools=tools)
        message = completion.choices[0].message
        tool_calls = message.tool_calls
        messages.append(message) # extend conversation with assistant's reply

    return message.content

def main():    
    messages = [
        {"role": "system", "content": "You are a project management assistant and you answer questions about the time tracking data of the company."\
         "You can answer questions about the actual date and time and you can call SQL queries on the data."}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_now",
                "description": "Gets the actual date and time",
                "parameters": {}
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_data",
                "description": "Calls a SQL query on the data and returns the result as JSON\n"\
                    "The header and first line of table=\"data\" looks like this:\n"\
                    "Datum;	Projekt Nr;	Kunde;	Projekt;	Subprojekt Nr;	Subprojekt;	Aktivität Nr;	Aktivität;	Verrechenbarkeit;	Mitarbeiter;	Zeit [h]\n"\
                    "02.01.2020;	8900;	M&F;	Allgemein;	1;	Bezahlte Abwesenheiten;	1;	Ferien; Abwesenheit;	Max Barthel;	8.4",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The SQL query to call on the data",
                        }
                    },
                    "required": ["query"]
                },
            }
        }]
    
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