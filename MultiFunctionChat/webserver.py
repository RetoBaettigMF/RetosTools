from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)
chatbot = None
server_running = True
webserver_thread = None

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
    while server_running:
        socketio.run(app, use_reloader=False)

def start_webserver(chatbot_instance):
    # Starte die SocketIO-Anwendung in einem separaten Thread
    global chatbot
    global webserver_thread
    chatbot = chatbot_instance
    print("Webserver wird gestartet")
    webserver_thread = threading.Thread(target=run_socketio)
    webserver_thread.start()

def stop_webserver():
    global server_running
    server_running = False
    print("Webserver wird beendet")
    socketio.stop()
    webserver_thread.join()
    print("Fertig")
    
    