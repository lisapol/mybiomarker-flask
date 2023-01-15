from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from mybiomarker.app import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/dashboard')
@login_required
def profile():
    if current_user and current_user.is_authenticated:
        return redirect('/hello-dashboard')

