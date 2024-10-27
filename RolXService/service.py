import sys
import os

from flask import Flask, request, jsonify
from rolx import Rolx
from tools import Tools
from openapi_def import OPENAPI_DEF

sys.path.append('../common')
from gpt import get_single_completion, get_completion_with_tools # type: ignore

print(get_single_completion("Hello, I am a test prompt."))

app = Flask(__name__)
rolx = Rolx()
tools = Tools(rolx)

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

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
        return result, 200
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
    
