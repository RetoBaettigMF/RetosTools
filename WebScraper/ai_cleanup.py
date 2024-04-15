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
        #model="gpt-3.5-turbo-1106",
        model="gpt-4-turbo",
        temperature=0
    )
    return chat_completion.choices[0].message.content
   

def aiCleanup(webpage):
    prompt = "I am scraping webpages and converting them to markdown. " \
    "Now I want you to remove the parts of the webpage that are not relevant to the content. " \
    "In particular, I want you to remove the navigation bar, the footer, the header and the sidebar. " \
    "I also want you to remove any links that are not relevant to the content. " \
    "I want you to remove any images, videos and ads that are not relevant to the content. " \
    "Here is the webpage I want you to clean up: \n+___+\n" + webpage
    try:
        return getCompletion(prompt)
    except Exception as e:
        print("Error: ", e)
        return None
    
    