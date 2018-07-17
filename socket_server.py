import socketio
import eventlet.wsgi
from flask import Flask

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('enter_room')
def enter_room(sid, data):
    sio.enter_room(sid, data)
    print('entered room '+data, sid)

@sio.on('leave_room')
def leave_room(sid, data):
    sio.leave_room(sid, data)
    print('left room '+data, sid)

@sio.on('project_updated')
def project_updated(sid, data):
    sio.emit('update_projects', {'data': data}, room='project/'+data)
    print("got project updated from user "+data)

@sio.on('new_message')
def new_message(sid, data):
    print("new message "+data.get('content', ''))
    sio.emit('message_added', {'data': data}, room='chat/'+str(data.get('chat_id', '')))

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
