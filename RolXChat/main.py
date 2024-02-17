from gpt import get_completion, get_single_completion
import json

def get_current_weather(location, unit="celsius"):
    return json.dumps({"location": location, "temperature": "22", "unit": unit})

def handle_tool_call(tool_call, messages):
    if not tool_call:
        return None
    
    available_functions = {
        "get_current_weather": get_current_weather,
    }  # only one function in this example, but you can have multiple
    # Step 4: send the info for each function call and function response to the model
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    function_response = function_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit"),
    )
    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        }
    )  # extend conversation with function response

def main():    
    messages = [
        {"role": "user", "content": "What is the weather like in Boston?"}
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }]
    

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

    print(message.content)


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
    chat()