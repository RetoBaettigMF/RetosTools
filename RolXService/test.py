import os
import requests
import sys
import json

sys.path.append('../common')
from gpt import get_single_completion # type: ignore

#BASE_URL = 'http://localhost:5000/rolx'
BASE_URL = 'https://baettig.org/rolx'
SQL_URL = BASE_URL+'/sqlquery'
PLAIN_URL = BASE_URL+'/query'

RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

def test_sql(sql_query):
    headers = {'Authorization': RETOS_API_TOKEN}
    
            
    # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
    response = requests.get(f"{SQL_URL}?query={sql_query}", headers=headers)
    response_data = response.json()
    return response_data


def test_ai(query):
        headers = {'Authorization': RETOS_API_TOKEN}
            
        # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
        response = requests.get(f"{PLAIN_URL}?query={query}", headers=headers)
        response_data = response.json()
        ans = get_single_completion("Enthält das folgende Objekt eine Aussage über eine Anzahl von Einträgen? Bitte Antwote NUR mit 'JA' oder 'NEIN': "+
                                    json.dumps(response_data))
        return ans

if __name__ == '__main__':
    query = "wieviele einträge hat es in der Datenbank? Gib mir die Antwort als JSON-Objekt."
    ans=test_ai(query)
    print(ans)
        
    query = "SELECT * FROM data LIMIT 5"
    response_data = test_sql(query)
    print("Response: "+json.dumps(response_data))
    
    query = "DROP TABLE data"
    response_data = test_sql(query)
    print("Response: "+json.dumps(response_data))