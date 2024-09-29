from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)
chatbot = None
my_app = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    global chatbot
    print('Message: ' + msg)
    reply = chatbot(msg)
    reply=reply.replace("\n", "<br>")
    emit('message', reply, broadcast=True)

def run_socketio():
    socketio.run(app, use_reloader=False)

def start_webserver(chatbot_instance):
    # Starte die SocketIO-Anwendung in einem separaten Thread
    global chatbot
    chatbot = chatbot_instance
    print("Webserver wird gestartet")
    webserver_thread = threading.Thread(target=run_socketio)
    webserver_thread.start()
    

    
    
    