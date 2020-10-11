from flask import Flask, render_template, request, make_response, abort
from flask_socketio import SocketIO, emit
import os
import sqlite3
import json
from auth import authenticate
import datetime
from routes import app

socketio = SocketIO(app, logger=True)

clients = []


@socketio.on('send_message')
def send_message_handler(data):
    data["by"] = request.cookies.get('USER_ID')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    now = datetime.datetime.now()
    currentTime = now.strftime("%Y-%m-%d %H:%M:%S")
    c.execute(f"""INSERT INTO Messages(by_user,body,time,room)
    VALUES
    ({data["by"]},'{data["message"]}','{currentTime}',{data["room"]})
    """)
    conn.commit()
    c.execute(f"""SELECT username FROM Users WHERE id={data["by"]}""")
    messageBY = c.fetchone()[0]
    for i in clients:
        if i["room"] == data["room"]:
            socketio.emit('message_received', {
                          "by": messageBY, "message": data["message"], "time": currentTime}, room=i["id"])


@socketio.on('connected')
def connect(data):
    clients.append({'id': request.sid, 'room': data['room']})


@socketio.on('disconnect')
def disconnect():
    for i in range(len(clients)):
        if clients[i]['id'] == request.sid:
            del clients[i]
            break


if __name__ == '__main__':
    socketio.run(app, debug=True)


def runApp(host,port):
    print(host)
    print(port)
    socketio.run(app)
