from functools import wraps
from flask import request
import sqlite3

def authenticate(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        username = request.cookies.get('USERNAME')
        if username and not username=='None':
            c.execute(f"""SELECT * FROM Users WHERE username='{username}'""")
            user = c.fetchone()
        else:
            user = None
        return f(user,*args,**kwargs)
    return wrapper