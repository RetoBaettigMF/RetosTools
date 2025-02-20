import asyncio

async def parallel_research(question: str):
    web_task = asyncio.create_task(web_search(question))
    rag_task = asyncio.create_task(rag_query(question))
    sql_task = asyncio.create_task(sql_query(question))
    
    results = await asyncio.gather(web_task, rag_task, sql_task)
    return synthesize_results(*results)