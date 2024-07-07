import requests
import urllib.parse
import pandas as pd
import os
import json

def get_date_range():
    # Hier eine Beispiel-Funktion. Implementiere dies nach Bedarf.
    return {
        "begin": "2023-01-01",
        "end": "2030-12-31"
    }

def get_rolx_data():
    # Besorge die Script-Eigenschaften
    api_key=os.getenv('ROLX_API_KEY');
    url = "https://rolx.m-f.ch/api/v1/rolx-chat-export?"
    
    params = get_date_range()
    
    # Füge die Parameter als Query-Parameter hinzu
    url += '&'.join([f"{urllib.parse.quote(key)}={urllib.parse.quote(str(value))}" for key, value in params.items()])

    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json",
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Überprüfe den Statuscode der Antwort
        if response.status_code != 200:
            print(f"Error: Response Code: {response.status_code}\nResponse: {response.text}")
            return None
        
        # Convert the string to a list of dictionaries
        data_list = json.loads(response.text)

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data_list)
        return df

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
