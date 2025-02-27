from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import Groq
from langchain_community.tools import Toolkit


db = SQLDatabase.from_uri("sqlite:///chinook.db")
agent_executor = create_sql_agent(llm=Groq(model="deepseek-r1"), toolkit=Toolkit(db=db))

def sql_query(question: str):
    try:
        return agent_executor.invoke({"input": question})["output"]
    except Exception as e:
        print(e)
        return "An error occurred while processing the query."+e.message