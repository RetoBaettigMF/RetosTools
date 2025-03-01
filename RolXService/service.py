import sys
import os
import json

from flask import Flask, request, jsonify
from rolx import Rolx
from tools import Tools
from openapi_def import OPENAPI_DEF

sys.path.append('../common')
from gpt import get_completion_with_tools, get_single_completion # type: ignore

app = Flask(__name__)
rolx = Rolx()
tools = Tools(rolx)

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError:
        return False
    
def query_is_dangerous(query):
    ans = get_single_completion("Is the following SQL query dangerous? Answer only YES or NO: "+query)
    if ans.upper() == 'YES':
        return True
    return False
    

@app.route('/rolx', methods=['GET'])
def test():
    return OPENAPI_DEF, 200

@app.route('/rolx/query', methods=['GET'])
def plain_text_query():
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401
    
    query = request.args.get('query')
    
    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400

    try:
        messages=[{"role": "user", "content": query}]
        result = get_completion_with_tools(messages, tools)
        if is_valid_json(result):
            return result, 200
        else:
            return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Fehlerbehandlung

@app.route('/rolx/sqlquery', methods=['GET'])
def get_data():
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    query = request.args.get('query')

    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400

    if query_is_dangerous(query):
        return jsonify({"result": "Dangerous query detected"}), 403
    
    # Führe die SQL-Abfrage aus
    try:
        result = rolx.get_data(query)  # Hier wird die Funktion aufgerufen
        return result, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Fehlerbehandlung
    
# Catch-All Route
@app.route('/<path:subpath>', methods=['GET'])
def catch_all(subpath):
    print(f"Endpoint '{subpath}' not found.")
    return f"Endpoint '{subpath}' not found.", 404

if __name__ == '__main__':
    app.run(port=5000)
    
