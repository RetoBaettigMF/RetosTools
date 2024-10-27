from openai import AzureOpenAI
import os
from settings import CHAT_MODEL, AZURE_OPENAI_ENDPOINT, AZURE_API_VERSION, AZURE_API_DEPLOYMENT_NAME, AZURE_API_EMBEDDING_DEPLOYMENT_NAME

def check_key():
    api_key = os.getenv('AZURE_OPENAI_KEY')
    if api_key is None:
        print("Error: AZURE_OPENAI_KEY key not found in environment variables.")
        return False
    return True

def get_vector_azure(text):
    if not check_key():
        return None 
    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version=AZURE_API_VERSION,
        azure_endpoint = AZURE_OPENAI_ENDPOINT
    )

    return client.embeddings.create(input = [text], model=AZURE_API_EMBEDDING_DEPLOYMENT_NAME).data[0].embedding

def get_completion_azure(**args):
    if not check_key():
        return None 
    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version=AZURE_API_VERSION,
        azure_endpoint = AZURE_OPENAI_ENDPOINT
    )

    args["model"] = AZURE_API_DEPLOYMENT_NAME
    
    chat_completion = client.chat.completions.create(**args)
     
    return chat_completion

def get_single_completion_azure(prompt):
    chat_completion = get_completion_azure(messages=[{"role": "user", "content": prompt}])
    return chat_completion.choices[0].message.content
