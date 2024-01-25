from gpt_openai import get_completion_openai, get_vector_openai
from gpt_azure import get_completion_azure, get_vector_azure
from settings import USE_AZURE

def get_completion(prompt):
    if USE_AZURE:
        return get_completion_azure(prompt)
    else:
        return get_completion_openai(prompt)

def get_vector(text):
    text = text.replace("\n", " ")
    if USE_AZURE:
        return get_vector_azure(text)
    else:
        return get_vector_openai(text)
    