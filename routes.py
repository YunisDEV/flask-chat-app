from flask import Flask, render_template, request, make_response, abort
from flask_socketio import SocketIO, emit
import os
import sqlite3
import json
from auth import authenticate
import datetime

app = Flask(__name__, static_folder='./public',
            static_url_path='/', template_folder='./views')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'hello')


@app.route('/')
def index():
    return render_template('account.html')


@app.route('/chat/<room>')
@authenticate
def chat(user, room):
    if not user:
        return """<script>window.open('/','_self')</script>"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f"""SELECT * FROM Rooms WHERE id={room}""")
    roomData = c.fetchone()
    if roomData:
        c.execute(f"""SELECT Users.username,Messages.body,Messages.time FROM 
        Messages INNER JOIN Users on Messages.by_user=Users.id WHERE room={roomData[0]}
        """)

        return render_template('chat.html', room=roomData, user=user, messages=c.fetchall())
    else:
        abort(404)


@app.route('/rooms')
@authenticate
def rooms(user):
    if not user:
        return """<script>window.open('/','_self')</script>"""
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute(f"""SELECT Rooms.id,Rooms.name,Rooms.password 
    FROM Rooms INNER JOIN RoomUserRelation ON Rooms.id=RoomUserRelation.room WHERE user={user[0]}
    """)
    rooms = c.fetchall()
    return render_template('rooms.html', user=user, rooms=rooms)


@app.route('/join', methods=['POST', 'GET'])
@authenticate
def join_room(user):
    if user:
        if request.method == 'POST':
            data = json.loads(request.data)
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(
                f"""SELECT * FROM Rooms WHERE name='{data["roomname"]}'""")
            room = c.fetchone()
            if room[2] == data["password"]:
                c.execute(f"""INSERT INTO RoomUserRelation(user,room)
                VALUES
                ({user[0]},{room[0]})
                """)
                conn.commit()
                resp = make_response({"success": True, "roomId": room[0]})
                return resp
            else:
                resp = make_response(
                    {"success": False, "message": 'Parol səhvdir'})
                return resp
        elif request.method == 'GET':
            return render_template('join_room.html')


@app.route('/create', methods=['POST', 'GET'])
@authenticate
def create_room(user):
    if user:
        if request.method == 'POST':
            data = json.loads(request.data)
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute(f"""INSERT INTO Rooms(name,password,owner) 
            VALUES
            ('{data["roomname"]}','{data["password"]}',{user[0]})
            """)
            roomId = c.lastrowid
            conn.commit()
            c.execute(f"""INSERT INTO RoomUserRelation(user,room)
            VALUES
            ({user[0]},{roomId})
            """)
            conn.commit()
            resp = make_response({"success": True, "roomId": roomId})
            return resp
        elif request.method == 'GET':
            return render_template('create_room.html')


@app.route('/user', methods=['POST'])
def account_submit():
    try:
        data = json.loads(request.data)
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute(
            f"""SELECT * FROM Users WHERE username='{data["username"]}'""")
        user = c.fetchone()
        if user:
            if user[2] == data["password"]:
                resp = make_response({'success': True})
                resp.set_cookie('USERNAME', user[1])
                resp.set_cookie('USER_ID', str(user[0]))
                return resp
            else:
                raise Exception('Parol səhvdir')
        else:
            c.execute(f"""INSERT INTO Users(username,password) 
            values 
            ('{data["username"]}','{data["password"]}')
            """)
            conn.commit()
            resp = make_response({'success': True})
            resp.set_cookie('USERNAME', data["username"])
            resp.set_cookie('USER_ID', str(c.lastrowid))
            return resp
    except Exception as e:
        print('Error:', e)
        if str(e).startswith("UNIQUE"):
            resp = make_response(
                {'success': False, 'message': 'Belə istifadəçi adı var'})
        else:
            resp = make_response({'success': False, 'message': str(e)})
        resp.set_cookie('USERNAME', 'None')
        resp.set_cookie('USER_ID', 'None')
        return resp


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


@app.route('/logout')
@authenticate
def logout(user):
    resp = make_response("""<script>window.open('/','_self')</script>""")
    resp.set_cookie('USERNAME', 'None', max_age=0)
    resp.set_cookie('USER_ID', 'None', max_age=0)
    return resp
