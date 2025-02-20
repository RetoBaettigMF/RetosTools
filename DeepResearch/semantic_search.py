from exa_py import Exa
import os

#exa = Exa(api_key=os.getenv("EXA_API_KEY"))
exa = Exa(api_key="a20201ce-9954-451a-b3b6-ccff4120593f")

def semantic_search(query: str, num_results: int = 5):
    return exa.search_and_contents(
        query,
        highlights=True,
        num_results=num_results,
        use_autoprompt=True
    )