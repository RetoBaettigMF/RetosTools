DB_FILE = "./vectordb.json"
HISTORY_FILE = "./history.json"
REPLAY_HISTORY_FILE = "./replay_history.json"
DATA_PATH = "./data"
PREPARED_DATA_PATH = "./prepareddata"
CHAT_MODEL = "gpt-3.5-turbo-16k"
#CHAT_MODEL = "gpt-4"
EMBEDDINGS_MODEL = "text-embedding-ada-002"

ANSWER_DONT_KNOW = "I don't know"
RAG_PROMPT = "Answer the following prompt based on the texts following the prompt. \n"\
"The texts are preceeded by a filename each. "\
"Include the filename in your answer in curly brackets like {{filename}}. \n"\
"If you can't answer the question based on the texts, return '"+ANSWER_DONT_KNOW+"'\n\n"\
"\nPrompt: {}"\
"\n\nTexts:\n {}"