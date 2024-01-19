import openai
import os

def getCompletion(prompt):
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key is None:
        print("Warning: OPENAI_API_KEY key not found in environment variables. Working without AI improvements.")
        return None
    
    client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo-1106",
        temperature=0
    )
    return chat_completion.choices[0].message.content
   

def GPT(prompt):
    return getCompletion(prompt)
    
    