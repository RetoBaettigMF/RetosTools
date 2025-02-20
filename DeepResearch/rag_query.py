from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
vectorstore = Chroma(persist_directory="./rag_store", embedding_function=embeddings)

def rag_query(question: str, docs: list[str]):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever.get_relevant_documents(question)