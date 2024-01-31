from openai import OpenAI
import os
from settings import CHAT_MODEL, EMBEDDINGS_MODEL

def check_key():
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        print("Error: OPENAI_API_KEY key not found in environment variables.")
        return False
    return True

def get_vector_openai(text):
    if not check_key():
        return None 
    client = OpenAI()
    return client.embeddings.create(input = [text], model=EMBEDDINGS_MODEL).data[0].embedding

def get_completion_openai(prompt):
    if not check_key():
        return None 
    
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=CHAT_MODEL
    )
    return chat_completion.choices[0].message.content
