from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from mybiomarker import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def dirty_bird():
    if current_user and current_user.is_authenticated:
        return render_template('test.html')


@main.route('/results',  methods=["POST", "GET"])
@login_required
def profile_2():
    if request.method == 'POST':
        my_value = request.form['my_value']
        my_unit = request.form['my_unit']
        my_test = request.form['my_test']
        # print("my med values")
        # print(my_value)
        # print(my_unit)
        # print(my_test)

    if current_user and current_user.is_authenticated:
        return render_template('test-2.html')


@main.route('/dashboard')
@login_required
def jj():
    if current_user and current_user.is_authenticated:
        return redirect('/hello-dashboard')
