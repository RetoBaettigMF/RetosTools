USE_AZURE = True

#OpenAI Settings
#(API-KEY is set in environment variable OPENAI_API_KEY)
CHAT_MODEL = "gpt-3.5-turbo-16k" #CHAT_MODEL = "gpt-4"
EMBEDDINGS_MODEL = "text-embedding-ada-002"


#Azure OpenAI Settings
#(API-KEY is set in environment variable AZURE_OPENAI_KEY)
AZURE_OPENAI_ENDPOINT = "https://mf-openai.openai.azure.com/"
AZURE_API_TYPE = 'azure'
AZURE_API_VERSION = '2023-09-01-preview'
AZURE_API_DEPLOYMENT_NAME = 'gpt4' # 'gpt-35-turbo-16k'
AZURE_API_EMBEDDING_DEPLOYMENT_NAME = 'text-embedding-ada-002'

#Database
DATABASE="rolx-export.xlsx"