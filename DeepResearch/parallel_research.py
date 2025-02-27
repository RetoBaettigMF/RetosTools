import asyncio
from semantic_search import web_search
from rag_query import rag_query
from sql_query import sql_query

def synthesize_results(web_results, rag_results, sql_results):
    return {
        "web": web_results,
        "rag": rag_results,
        "sql": sql_results
    }

async def parallel_research(question: str):
    web_task = asyncio.create_task(web_search(question))
    rag_task = asyncio.create_task(rag_query(question))
    sql_task = asyncio.create_task(sql_query(question))
    
    results = await asyncio.gather(web_task, rag_task, sql_task)
    return synthesize_results(*results)