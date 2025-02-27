from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!")

@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.json
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(port=4321)