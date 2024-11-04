import requests
import urllib.parse
import pandas as pd
from pandasql import sqldf
import os
import json
import threading
import time

class Rolx():
    __instance = None
    data = None

    def __get_date_range(self):
        # Hier eine Beispiel-Funktion. Implementiere dies nach Bedarf.
        return {
            "begin": "2023-01-01",
            "end": "2030-12-31"
        }

    def __get_rolx_data(self):
        # Besorge die Script-Eigenschaften
        api_key=os.getenv('ROLX_API_KEY');
        url = "https://rolx.m-f.ch/api/v1/rolx-chat-export?"
        
        params = self.__get_date_range()
        
        # Füge die Parameter als Query-Parameter hinzu
        url += '&'.join([f"{urllib.parse.quote(key)}={urllib.parse.quote(str(value))}" for key, value in params.items()])

        headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        }
        
        try:
            print("Loading Rolx data...")
            response = requests.get(url, headers=headers)
            
            # Überprüfe den Statuscode der Antwort
            if response.status_code != 200:
                print(f"Error: Response Code: {response.status_code}\nResponse: {response.text}")
                return None
            
            # Convert the string to a list of dictionaries
            data_list = json.loads(response.text)

            # Create a pandas dataframe from the list of dictionaries
            self.data = pd.DataFrame(data_list)
            print("...data successfully loaded")
            self.__start_timer()
            
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed, could not get RolX Data: {e}")
            raise e
        
    def get_data(self, sql_query=None):
        try:
            if sql_query is None:
                headers = self.data.columns.tolist()
                return json.dumps({"table: data, headers": headers})
        
            result = sqldf(sql_query, self.__dict__)
        except Exception as e:
            return json.dumps({"error": str(e)})
        
        result = result.to_json(orient="records")
        return result
    
    def __start_timer(self):
        self.timer = threading.Timer(300, self.__get_rolx_data)  # 300 Sekunden = 5 Minuten
        self.timer.start()
       
    def __new__(self):
        if not self.__instance:
            print('Creating new instance')
            self.__instance = super(Rolx, self).__new__(self)
            self.__instance.__get_rolx_data()
        
        print('Returning instance')
        return self.__instance
    
    def _rolx_test(self):
        # Teste die Klasse Rolx
        print(self.get_data())
        print(self.get_data("SELECT * FROM data LIMIT 5"))
        print(self.get_data("SELECT * FROM data WHERE user_id = 1"))
        print(self.get_data("SELECT DISTINCT firstName, lastname FROM data"))