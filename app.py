from flask import Flask, render_template
from flask_socketio import SocketIO, send

# Create a Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# List to store chat messages
messages = []

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event for when a new client connects
@socketio.on('connect')
def handle_connect():
    # Send the existing messages to the new client
    socketio.emit('messages', messages)

# SocketIO event for when a new message is received
@socketio.on('message')
def handle_message(data):
    messages.append(data)  # Add the new message to the list
    socketio.emit('message', data)  # Broadcast the new message to all clients

# Handle clearing messages
@socketio.on('clear')
def handle_clear():
    messages.clear()
    socketio.emit("clear", "Chat cleared")

if __name__ == '__main__':
    socketio.run(app, debug=True)
