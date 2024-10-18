from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

@app.route('/api/data', methods=['GET'])
def get_data():
    print("Got request")
    # Prüfen, ob der Authorization-Header vorhanden ist und dem geheimen Token entspricht
    auth_header = request.headers.get('Authorization')
    if auth_header != RETOS_API_TOKEN:
        return jsonify({'message': 'Unauthorized'}), 401

    # Generieren Sie hier Ihre Antwort
    data = {'message': 'Erfolgreich authentifiziert!'}
    return jsonify(data), 200

if __name__ == '__main__':
    # Starten Sie die Anwendung mit SSL-Kontext
    app.run(ssl_context=('cert.pem', 'key.pem'))
