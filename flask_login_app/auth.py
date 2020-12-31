from flask import Blueprint, render_template
# from .app import db

auth = Blueprint('auth', __name__, static_folder='Static', template_folder='Templates')

@auth.route('/login')
def login():
    db
    return 'Login'

@auth.route('/logout')
def logout():
    return 'Logout'
