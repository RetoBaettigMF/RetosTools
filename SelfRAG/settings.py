DB_FILE = "./vectordb.json"
DATA_PATH = "./data"
PREPARED_DATA_PATH = "./prepareddata"
CHAT_MODEL = "gpt-4"
EMBEDDINGS_MODEL = "text-embedding-ada-002"

RAG_PROMPT = "Answer the following prompt based on the texts following the prompt. \n"\
"The texts are preceeded by a filename each. "\
"Include the filename in your answer in curly brackets. \n"\
"If you can't answer the question based on the texts, return 'I don't know'\n\n"\
"\nPrompt: {}"\
"\n\nTexts:\n {}"