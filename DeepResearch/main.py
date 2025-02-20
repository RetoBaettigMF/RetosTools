from langchain import hub
from langchain_community.tools import Tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_agent_executor

# Initialisierung der Komponenten
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