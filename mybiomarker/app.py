import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from flask_mail import Mail

# export FLASK_APP=app.py
app = Flask(__name__)

db_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_directory, 'dbusers.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT']   = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ['EMAIL_USER']
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = ('Elizaveta Poluboiarinova', 'elizaveta.olariu@gmail.com')

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


@app.route("/")
def index():
    return render_template("index.html")

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, email=User)

if __name__ == "__main__":
    # app.run()
    pass