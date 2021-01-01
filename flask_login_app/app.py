from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_ngrok import run_with_ngrok # from local machine to web, run only while runnign locally.

# init SQLAlchemy and app
app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

path = "C:/Users/dpsar/Documents/projects/github/flaskApp/flask_login_app"
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}/Data/Users.db' # assuming that the db is in the folder Data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column('password', db.String(1000))

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    # since the id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(id))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.username)

@app.route('/')
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return render_template("home.html")
    else:
        return render_template('login.html')

# this will run only when user posts to the url /login
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login_post')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
