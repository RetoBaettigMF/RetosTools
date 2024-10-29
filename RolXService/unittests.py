import unittest
import os
import requests
import sys
import json

sys.path.append('../common')
from gpt import get_single_completion # type: ignore


class APITestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5000/rolx'
    SQL_URL = BASE_URL+'/sqlquery'
    PLAIN_URL = BASE_URL+'/query'
    
    RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
    if RETOS_API_TOKEN is None:
        raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')
    
    """
    def test_unauthorized_access(self):
        response = requests.get(self.SQL_URL, verify=False)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Unauthorized'})

    def test_missing_query(self):
        headers = {'Authorization': self.RETOS_API_TOKEN}
        response = requests.get(self.SQL_URL, headers=headers, verify=False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Query parameter is required'})
    
    def test_successful_query(self):
        headers = {'Authorization': self.RETOS_API_TOKEN}
        query = "SELECT * FROM data LIMIT 5"
                
        # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
        response = requests.get(f"{self.SQL_URL}?query={query}", headers=headers, verify=False)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 5)
"""
    def test_successful_query2(self):
        headers = {'Authorization': self.RETOS_API_TOKEN}
        query = "wieviele einträge hat es in der Datenbank?"
                
        # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
        response = requests.get(f"{self.PLAIN_URL}?query={query}", headers=headers, verify=False)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        ans = get_single_completion("Enthält das folgende Objekt eine Aussage über eine Anzahl von Einträgen? Bitte Antwote NUR mit 'JA' oder 'NEIN': "+
                                    json.dumps(response_data))
        self.assertEqual(ans.upper(), "JA")
    
if __name__ == '__main__':
    unittest.main()
