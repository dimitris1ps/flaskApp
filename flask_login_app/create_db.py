"""
- Create a sqlite3 database: from command line for example `sqlite3 Users.db` then ``.quit`
- then run this code
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

path = "C:/Users/dpsar/Documents/projects/github/flaskApp/Flask-Login-App-Tutorial"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}/Data/Users.db' # assuming that the db is in the forlder Data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column('password', db.String(1000))

    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        return check_password_hash(self.password, secret)

db.create_all()

# create a 2 users with a hash for the password so the plaintext version isn't saved.
for el in zip(['dimitris1', 'dimitris2'], ['admin1', 'admin2']):
    u = User(username=el[0])
    u.set_password(el[1])
    db.session.add(u) # add the new user to the database
    db.session.commit()

# # check_password_hash(hashed password, actual password)
# x = db.session.query(User).filter_by(username='dimitris2').one()
# print(x.password)
# print(x.check_password('admin2'))
