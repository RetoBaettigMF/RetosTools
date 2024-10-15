DB_FILE = "./vectordb.json"
HISTORY_FILE = "./history.json"
REPLAY_HISTORY_FILE = "./replay_history.json"
DATA_PATH = "./data"
MD_DATA_PATH = "./md_data"
PREPARED_DATA_PATH = "./prepareddata"

USE_AZURE = True

#OpenAI Settings
#(API-KEY is set in environment variable OPENAI_API_KEY)
CHAT_MODEL = "gpt-3.5-turbo-16k" #CHAT_MODEL = "gpt-4"


#Azure OpenAI Settings
#(API-KEY is set in environment variable AZURE_OPENAI_KEY)
AZURE_OPENAI_ENDPOINT = "https://mf-openai-sweden-central.openai.azure.com/"
AZURE_API_TYPE = 'azure'
AZURE_API_VERSION = '2024-05-01-preview'
#AZURE_API_DEPLOYMENT_NAME = 'gpt-4o' # 'gpt-35-turbo-16k'
AZURE_API_DEPLOYMENT_NAME = 'gpt-4o-mini' # 'gpt-35-turbo-16k'
AZURE_API_EMBEDDING_DEPLOYMENT_NAME = 'text-embedding-ada-002'



deployment_name='REPLACE_WITH_YOUR_DEPLOYMENT_NAME' #This will correspond to the custom name you chose for your deployment when you deployed a model. 

EMBEDDINGS_MODEL = "text-embedding-ada-002"
TEXT_CHUNK_MAXSIZE = 4000
TEXT_CHUNK_OVERLAP = 1000

ANSWER_DONT_KNOW = "I don't know"

"""
    RAG_PROMPT = "Answer the following prompt based on the texts following the prompt. \n"\
    "The texts are preceeded by a filename each. "\
    "Include the filename in your answer in curly brackets like {{filename}}. \n"\
    "If you can't answer the question based on the texts, return '"+ANSWER_DONT_KNOW+"'\n\n"\
    "\nPrompt: {}"\
    "\n\nTexts:\n {}"
"""

RAG_PROMPT = "Beantworte die folgende Aufgabe basierend auf den Texten, die der Aufgabe folgen. \n"\
"Den Texten geht jeweils eine Dateiname voraus. "\
"Füge den Dateinamen in deiner Antwort in geschweiften Klammern ein, wie {{Dateiname}}. \n"\
"Wenn du die Frage nicht anhand der Texte beantworten kannst, gib '"+ANSWER_DONT_KNOW+"' zurück.\n\n"\
"\nPrompt: {}"\
"\n\nTexts:\n {}"