from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, current_user
from mybiomarker import db
from mybiomarker.models import DataV1, MyVitamins

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
        if request.form['my_value']:
            my_value = request.form['my_value']
            my_unit = request.form['my_unit']
            my_test = request.form['my_test']
            my_start_date = request.form['my_start_date']

            user = DataV1.query.filter_by(my_value=my_value).filter_by(email=current_user.email).first()

            if not user:
                new_record = DataV1(
                    email=current_user.email, my_value=my_value, my_unit=str(my_unit), my_test=my_test, my_start_date=my_start_date)

                # add the new user to the database
                db.session.add(new_record)
                db.session.commit()
            if user:
                print("uesss")
    if current_user and current_user.is_authenticated:
        return render_template('test-2.html')


@main.route('/results-01', methods=["POST"])
@login_required
def profile_1():
    if request.form['vitamin_name']:

        vitamin_name = request.form['vitamin_name']
        start_date = request.form['start_date']
        duration = request.form['duration']

        user = MyVitamins.query.filter_by(vitamin_name=vitamin_name).filter_by(email=current_user.email).first()

        if not user:
            new_record = MyVitamins(
                email=current_user.email, vitamin_name=vitamin_name, start_date=start_date, duration=duration)
            db.session.add(new_record)
            db.session.commit()
        if user:
            print("uesss")

    if current_user and current_user.is_authenticated:
        return render_template('test-2.html')


@main.route('/dashboard')
@login_required
def jj():
    if current_user and current_user.is_authenticated:
        return redirect('/hello-dashboard')
