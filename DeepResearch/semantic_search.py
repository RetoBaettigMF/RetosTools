from exa_py import Exa

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

def semantic_search(query: str, num_results: int = 5):
    return exa.search_and_contents(
        query,
        highlights=True,
        num_results=num_results,
        use_autoprompt=True
    )