from gpt_openai import get_single_completion_openai, get_vector_openai, get_completion_openai
from gpt_azure import get_single_completion_azure, get_completion_azure, get_vector_azure
from settings import USE_AZURE

def get_single_completion(prompt):
    try:
        if USE_AZURE:
            return get_single_completion_azure(prompt)
        else:
            return get_single_completion_openai(prompt)
    except Exception as e:
        print("Error in get_single_completion: ", e)
        return e
        
def get_completion(**args):
    try:
        if USE_AZURE:
            return get_completion_azure(**args)
        else:
            return get_completion_openai(**args)
    except Exception as e:
        print("Error in get_completion: ", e)
        return e
    
def get_vector(text):
    text = text.replace("\n", " ")
    if USE_AZURE:
        return get_vector_azure(text)
    else:
        return get_vector_openai(text)
    
def get_completion_with_tools(messages, tools):
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
    