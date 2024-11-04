import os
import requests
import sys
import json

sys.path.append('../common')
from gpt import get_single_completion # type: ignore

BASE_URL = 'http://localhost:5000/rolx'
#BASE_URL = 'http://baettig.org/rolx'
SQL_URL = BASE_URL+'/sqlquery'
PLAIN_URL = BASE_URL+'/query'

RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

def test():
    headers = {'Authorization': RETOS_API_TOKEN}
    query = "SELECT * FROM data LIMIT 5"
    query = "DROP TABLE data"
            
    # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
    response = requests.get(f"{SQL_URL}?query={query}", headers=headers, verify=False)
    print("Status Code: ",response.status_code)
    response_data = response.json()
    print("Response: "+json.dumps(response_data))
    
if __name__ == '__main__':
    test()
