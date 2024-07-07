import requests
import os

def google_search(query, **kwargs):
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('GOOGLE_CSE_ID')
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query, "snippetlength"  : 1000}
    params.update(kwargs)
    
    response = requests.get(url, params=params).json()

    results = []
    for item in response.get("items", []):
        result = {"title": item["title"], "link": item["link"], "snippet": item["snippet"]}
        results.append(result)

    return results

    