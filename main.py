from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    return redirect(url_for('index'))

@socketio.on('message')
def handle_message(msg):
    username = session.get('username', 'Anonymous')
    send({'msg': msg, 'username': username}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=1011)
