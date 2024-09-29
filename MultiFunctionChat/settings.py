USE_AZURE = True

#OpenAI Settings
#(API-KEY is set in environment variable OPENAI_API_KEY)
CHAT_MODEL = "gpt-4" #CHAT_MODEL = "gpt-3.5-turbo-16k"
EMBEDDINGS_MODEL = "text-embedding-ada-002"


#Azure OpenAI Settings
#(API-KEY is set in environment variable AZURE_OPENAI_KEY)
AZURE_OPENAI_ENDPOINT = "https://mf-openai-sweden-central.openai.azure.com/"
AZURE_API_TYPE = 'azure'
AZURE_API_VERSION = '2024-05-01-preview'
#AZURE_API_DEPLOYMENT_NAME = 'gpt-4o' # 'gpt-35-turbo-16k'
AZURE_API_DEPLOYMENT_NAME = 'gpt-4o-mini' # 'gpt-35-turbo-16k'
AZURE_API_EMBEDDING_DEPLOYMENT_NAME = 'text-embedding-ada-002'

#GMAIL Reader Settings
MAX_EMAILS = 50

#Initial Message
INITIAL_MESSAGE = [
        {"role": "system", "content": "You are a helpful assistant and you try to execute the wishes of the user by using all your abilities."\
         "You can make multiple tool calls to support the user. Use the following functions \n"\
         "- get_now: to get current date and time\n"\
         "- execute_python_code: to execute programs\n"\
         "- get_timesheet_entries: to get timesheet and project data\n"            
         "- scrape: to scrape a website. Use it to get information from links you found via google_search\n"\
         "- google_search: to search google\n"\
         "- gmail_search: to search my emails"
         "If the user asks a question, make a plan to solve the problem and execute the plan."
        }
    ]



