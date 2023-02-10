from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from mybiomarker import db
from mybiomarker.models import MyData

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

        user = MyData.query.filter_by(my_value=my_value).first()

        if not user:
            new_record = MyData(my_value=my_value, my_unit=str(my_unit), my_test=my_test)

            # add the new user to the database
            db.session.add(new_record)
            db.session.commit()
        if user:
            print("uesss")
            flash('this record already exists')

    if current_user and current_user.is_authenticated:
        return render_template('test-2.html')


@main.route('/dashboard')
@login_required
def jj():
    if current_user and current_user.is_authenticated:
        return redirect('/hello-dashboard')
