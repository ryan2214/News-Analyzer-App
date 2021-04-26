from datetime import datetime
import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.security import check_password_hash, generate_password_hash
from news_analyzer.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/create_user', methods=('GET', 'POST'))
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html', title='User Registration', year=datetime.now().year)

    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    error_message = None

    if not username:
        error_message = 'Enter a user name'
    elif not password:
        error_message = 'Enter a password'
    elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
        error_message = 'User name {} is already registered by someone'.format(username)

    if error_message is not None:
        flash(error_message, category='alert alert-danger')
        return redirect(url_for('auth.create_user'))

    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()

    flash('You successfully completed user registration. Please login with your user name and password', category='alert alert-info')
    return redirect(url_for('auth.login'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login', year=datetime.now().year)

    username = request.form['username']
    password = request.form['password']

    db = get_db()
    error_message = None

    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error_message = 'Invalid user name'
    elif not check_password_hash(user['password'], password):
        error_message = 'Invalid password'

    if error_message is not None:
        flash(error_message, category='alert alert-danger')
        return redirect(url_for('auth.login'))

    session.clear()
    session['user_id'] = user['id']
    flash('You successfully logged in as {}'.format(username), category='alert alert-info')
    return redirect(url_for('home'))

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out', category='alert alert-info')
    return redirect(url_for('home'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Please log in first', category='alert alert-warning')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


