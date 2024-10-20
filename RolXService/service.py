from flask import Flask, request, jsonify
from rolx import Rolx
import os

app = Flask(__name__)
rolx = Rolx()

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

@app.route('/rolx/test', methods=['GET'])
def test():
    return "API Works!", 200

@app.route('/rolx/sqlquery', methods=['GET'])
def get_data():
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    #if not request.is_json:
    #    return jsonify({'message': r'Invalid input, JSON required like: {"query":"SELECT * FROM data LIMIT 5"}'}), 400

    # Extrahiere die SQL-Abfrage aus dem JSON-Objekt
    #data = request.get_json()
    #query = data.get('query')
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
    # Starten Sie die Anwendung mit SSL-Kontext
    #app.run(host='0.0.0.0', port=5000, ssl_context=('/etc/letsencrypt/live/baettig.org/fullchain.pem', '/etc/letsencrypt/live/baettig.org/privkey.pem'))
    app.run(port=5000)
    
