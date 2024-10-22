from flask import Flask, request, jsonify
from rolx import Rolx
import os

app = Flask(__name__)
rolx = Rolx()

# Laden Sie den geheimen Token aus einer Umgebungsvariable
RETOS_API_TOKEN = os.environ.get('RETOS_API_TOKEN')
if RETOS_API_TOKEN is None:
    raise ValueError('RETOS_API_TOKEN nicht in Umgebungsvariablen gefunden')

@app.route('/rolx', methods=['GET'])
def test():
    return """
    {
  "openapi": "3.1.0",
  "info": {
    "title": "Get timesheet entries",
    "description": "Retrieves timesheet entries for the company",
    "version": "v1.0.0"
  },
  "servers": [
    {
      "url": "https://baettig.org"
    }
  ],
  "paths": {
    "/rolx/sqlquery": {
      "get": {
        "description": "Get timesheet data",
        "operationId": "SQLQuery",
    
        "parameters": [
          {
            "name": "query",
            "in": "query",
            "description": "The SQL query for the table 'data'.
The fields of the timesheet database include:
date, firstName, lastName, projectNumber, subprojectNumber, activityNumber, orderNumber (in the form of #0123.456 where 123 is the projectNumber and 456 is the subprojectNumber), customerName, projectName, subprojectName, activityName, durationHours, billabilityName, isBillable (1 for billable, 0 for non-billable), comment.
If you have to calculate the billability, do the following:
- get all hours where billabilityName!=Abwesenheit as Anwesenheit
- get all hours where isBillable = 1 as Billable
- calculate the billability as Billable/Anwesenheit

If ever possible, do the calculations in the SQL statement.",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        
        "deprecated": false
      }
    }
  },
  "components": {
    "schemas": {}
  }
}""", 200

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
    
