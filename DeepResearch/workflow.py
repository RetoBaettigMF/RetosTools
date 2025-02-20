from langgraph.graph import StateGraph

workflow = StateGraph(ResearchState)

workflow.add_node("web_search", web_search_node)
workflow.add_node("rag_analysis", rag_analysis_node)
workflow.add_node("sql_query", sql_query_node)
workflow.add_node("synthesis", synthesis_node)

workflow.add_edge("web_search", "synthesis")
workflow.add_edge("rag_analysis", "synthesis")
workflow.add_edge("sql_query", "synthesis")

workflow.set_entry_point("web_search")
workflow.set_entry_point("rag_analysis")
workflow.set_entry_point("sql_query")