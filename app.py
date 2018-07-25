from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return 'changed in git text from socketio + changed in branch'

@socketio.on('connect')
def connect():
    print("connect")

@socketio.on('disconnect')
def disconnect():
    print('disconnect')

@socketio.on('enter_room')
def on_join(data):
    join_room(data)
    print('entered room '+data)

@socketio.on('leave_room')
def on_leave(data):
    leave_room(data)
    print('left room '+data)

@socketio.on('project_updated')
def project_updated(data):
    socketio.emit('update_projects', {'data': data}, room='project/'+data)
    print("got project updated from user "+data)

@socketio.on('new_message')
def new_message(data):
    print("new message "+data.get('content', ''))
    socketio.emit('message_added', {'data': data}, room='chat/'+str(data.get('chat_id', '')))

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)


