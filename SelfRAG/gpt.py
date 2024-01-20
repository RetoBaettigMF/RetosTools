import openai
import os
from settings import CHAT_MODEL


def get_completion(prompt):
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        print("Error: OPENAI_API_KEY key not found in environment variables.")
        return None
    
    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=CHAT_MODEL
    )
    return chat_completion.choices[0].message.content
   
    
    