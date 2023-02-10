from mybiomarker import db
# Flask-Login will be able to work with the User model.
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)   # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class MyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)   # primary keys are required by SQLAlchemy
    my_value = db.Column(db.String(100), unique=True)
    my_unit = db.Column(db.Integer)
    my_test = db.Column(db.String(1000))
