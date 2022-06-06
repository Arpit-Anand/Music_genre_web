from crypt import methods
import functools
from operator import methodcaller
from tkinter.messagebox import NO
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix = '/auth')


@bp.route('/register', methods = ('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        age = request.form['age']
        gender = request.form['gender']

        db = get_db()
        error = None

        if not firstName:
            error = 'First Name is required'
        elif not lastName:
            error = 'Last Name is required'
        elif not age:
            error = 'Age is required'
        elif not username :
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        
        if error is None:
            try:
                db.execute("INSERT INTO userInfo (firstName, lastName, age, gender, username, password) VALUES (?,?,?,?,?,?)",
                (firstName, lastName, age, gender, username, generate_password_hash(password)),)
                db.commit()
            except db.IntegrityError:
                error = f"Username {username} already in use."
            else:
                return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    error  = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM userInfo WHERE username = ?', (username,)).fetchone()

        if user is None:
            error = 'User doesn\'t exists.'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect Passowrd.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    else:
        error = 'Please fill the form'
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM userInfo WHERE id = ?',(user_id,)).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

'''@app.route('/start')
     def start():
        response = requests.get('https://api.kanye.rest/')
        response.raise_for_status()
        data = response.json()
        useable = data["quote"]
        return render_template('start.html', quote = useable)'''