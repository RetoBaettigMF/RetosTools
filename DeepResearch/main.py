from langchain import hub
from langchain_community.tools import Tool
from langchain_groq import ChatGroq
from create_agent_executor import create_agent_executor
from semantic_search import semantic_search
from rag_query import rag_query, create_rag_store
from sql_query import sql_query

# Initialisierung der Komponenten
create_rag_store()
llm = ChatGroq(model="deepseek-r1", temperature=0)
exa_tool = Tool.from_function(
    name="web_search",
    func=semantic_search,
    description="Semantische Websuche mit Exa-API"
)
rag_tool = Tool.from_function(
    name="document_analysis",
    func=rag_query,
    description="Dokumentenanalyse mittels RAG"
)
sql_tool = Tool.from_function(
    name="database_query",
    func=sql_query,
    description="SQL-Datenbankabfragen"
)

# Agentenkonfiguration
agent = create_agent_executor(
    tools=[exa_tool, rag_tool, sql_tool],
    llm=llm,
    system_message=hub.pull("research-agent-system"),
    interrupt_before_action=True
)

# Ausführungsbeispiel
result = agent.invoke({
    "input": "Vergleich der KI-Strategien deutscher DAX-Unternehmen 2023-2024"
})
print(result["output"])