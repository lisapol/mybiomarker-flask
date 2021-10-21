import os
import time

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mail import Mail, Message

# export FLASK_APP=app.py
app = Flask(__name__)

db_directory = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_directory, 'dbusers.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://syutixbvnoarbe:c821a3fea21e09ea1aca6d4ca83da4f68d3cd20928820c53f6b01e425548b08a@ec2-34-242-89-204.eu-west-1.compute.amazonaws.com:5432/dvtng5ubn3l7b'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT']   = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('MyBioMarker', 'elizaveta.olariu@gmail.com')

mail = Mail(app)
# from app import mail
# from flask_mail import Message
# msg = Message('Hello', recipients=['polmm.em@gmail.com'])
# msg.body = "This is the email body"
# mail.send(msg)


# -----------------------------------------------------------------------------------------
# send email function
def send_email(recipient, email_subject, email_body):
    """
      function: send email
       :param : recipient - deliver the email to this recipient
                email_subject - subject of the email
                email_body - Body of the mail..

    """
    message = Message(email_subject, recipients=[recipient])
    message.body = email_body
    mail.send(message)

db = SQLAlchemy(app)
print(db)

class User(db.Model):
    """
        Class: User
        Function: Data-model Definition for users table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True)

    def __repr__(self):
        return '<E-mail  %r>' % self.email

# flask shell
# from app import db
# db.create_all()
# from app import User
# user1 = User(user_full_name='Roger Federer')
# user2 = User(user_full_name='Rafael Nadal')
# db.session.add(user1)
# db.session.add(user2)
# db.session.commit()
# User.query.all()
@app.route('/')
def index():
    return render_template("index.html")


@app.route("/process", methods=['POST'])
def process():
    if request.method == 'POST':
        recipient = request.form['email']

        user = User.query.filter_by(email=recipient).first()

        if user is None:
            print(f" *** {user} Not found")
            user = User(email=recipient)
            db.session.add(user)
            db.session.commit()
            msg = Message('MyBioMarker Subscription', recipients=[recipient])
            msg.body = ('MyBioMarker Subscription.')
            msg.html = ('<h1>MyBioMarker Subscription</h1>'
                        '<p>Thank you for subscription to MyBioMarker newsletter!</p>')
            try:
                mail.send(msg)
            except:
                pass
            return jsonify({'name': 'Thanks for subscribing!❤️️'})
        else:
            return jsonify({'error': 'You have been subscribed earlier ❤️'})

    return jsonify({'name': user})

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, email=User)


if __name__ == "__main__":
    # app.debug = True
    app.run()
    # pass