from gpt_openai import get_single_completion_openai, get_vector_openai, get_completion_openai, get_json_completion_openai
from gpt_azure import get_single_completion_azure, get_completion_azure, get_vector_azure, get_json_completion_azure
from settings import USE_AZURE

def get_single_completion(prompt):
    if USE_AZURE:
        return get_single_completion_azure(prompt)
    else:
        return get_single_completion_openai(prompt)

def get_json_completion(prompt):
    if prompt.lower().find("json")==-1:
            prompt = prompt+" \nReturn the answer in json format { \"answer\": ...}"
    if USE_AZURE:
        return get_json_completion_azure(prompt)
    else:
        return get_json_completion_openai(prompt)
    
def get_completion(**args):
    if USE_AZURE:
        return get_completion_azure(**args)
    else:
        return get_completion_openai(**args)

def get_vector(text):
    text = text.replace("\n", " ")
    if USE_AZURE:
        return get_vector_azure(text)
    else:
        return get_vector_openai(text)
    