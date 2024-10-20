import unittest
import os
import requests

class APITestCase(unittest.TestCase):
    BASE_URL = 'http://localhost:5000/rolx/sqlquery'
    
    RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
    if RETOS_API_TOKEN is None:
        raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')
    
    def test_unauthorized_access(self):
        response = requests.get(self.BASE_URL, verify=False)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'Unauthorized'})

    def test_missing_query(self):
        headers = {'Authorization': self.RETOS_API_TOKEN}
        response = requests.get(self.BASE_URL, headers=headers, verify=False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'Query parameter is required'})
    
    def test_successful_query(self):
        headers = {'Authorization': self.RETOS_API_TOKEN}
        query = "SELECT * FROM data LIMIT 5"
                
        # Hier solltest du sicherstellen, dass der Service tatsächlich läuft und die erwartete Antwort zurückgibt
        response = requests.get(f"{self.BASE_URL}?query={query}", headers=headers, verify=False)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 5)
    
if __name__ == '__main__':
    unittest.main()
