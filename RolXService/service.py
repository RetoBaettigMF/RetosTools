from flask import Flask, request, jsonify
from rolx import Rolx
import os

app = Flask(__name__)
rolx = Rolx()

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

@app.route('/api/test', methods=['GET'])
def test():
    return "API Works!", 200

@app.route('/api/data', methods=['GET'])
def get_data():
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    if not request.is_json:
        return jsonify({'message': 'Invalid input, JSON required like: \{"query":"SELECT * FROM data LIMIT 5"\}'}), 400

    # Extrahiere die SQL-Abfrage aus dem JSON-Objekt
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'message': 'Query parameter is required'}), 400

    # Führe die SQL-Abfrage aus
    try:
        result = rolx.get_data(query)  # Hier wird die Funktion aufgerufen
        return result, 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500  # Fehlerbehandlung

if __name__ == '__main__':
    # Starten Sie die Anwendung mit SSL-Kontext
    app.run(ssl_context=('cert.pem', 'key.pem'))
    #app.run()
    
