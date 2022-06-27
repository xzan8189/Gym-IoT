from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.exceptions import BadRequestKeyError

from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash

from models.Utils import Utils

auth = Blueprint('auth', __name__)

# Variabili d'istanza
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Users')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if ('user_in_session' in  session):
        flash('You are already logged in!', category='success')
        return redirect(url_for('views.home'))

    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        print(f'Username: {username}, Password: {password}')

        try:
            user_found_dict = table.get_item(Key={'username': username})
            if len(user_found_dict)>1:
                if check_password_hash(user_found_dict['Item']['password'], password):
                    flash('Logged in successfully!', category='success')
                    session['user_in_session'] = user_found_dict['Item']
                    #return render_template("home.html", user=user_found_dict['Item'])
                    return redirect(url_for('views.home', user=user_found_dict['Item']))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Username does not exist.', category='error')
        except ClientError as e:
            print(e.response['Error']['Message'])


    print("ciao")
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': # Taking data from the form in "sign-up.html"
        username = request.form.get('username')
        name = request.form.get('name')
        surname = request.form.get('surname')

        try:
            sex = request.form['sexRadio']
        except BadRequestKeyError as e:
            flash("The sex is not selected.", category='error')
            return render_template("sign_up.html")

        age = request.form.get('age')
        weight = request.form.get('weight')
        height = request.form.get('height')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Several controls before adding new user
        try:
            response = table.get_item(Key={'username': username})
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])

        if len(username) < 4:
            flash("Username must be greater than 4 characters.", category='error')
        elif 'Item' in response:
            flash('Username already exists. So the user already exists.', category='error')
        elif len(name) < 2:
            flash("First name must be greater than 2 characters.", category='error')
        elif len(surname) < 2:
            flash("Surname must be greater than 2 characters.", category='error')
        elif sex == None:
            flash("The sex is not selected.", category='error')
        elif int(age) < 18:
            flash('Your age must be over 18.', category='error')
        elif len(str(weight))<1 or float(weight)<40:
            flash("Error in Weight.", category='error')
        elif len(str(height))<1 or float(height)<1:
            flash("Error in Height.", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            new_user = User(
                username=username,
                name=name,
                surname=surname,
                password=generate_password_hash(password1, method='sha256'),
                registration_date=str(datetime.date(datetime.now())),
                last_time_user_was_updated= str(datetime.today().strftime('%Y-%m-%d')),
                sex=str(sex),
                age=str(age),
                weight=weight,
                height=height,
                calories_to_reach_today=str(Utils.calculate_calorie_deficit(sex, float(weight), float(height), int(age)))
            )
            new_user_dict = Utils.create_objectUser_to_dict(new_user)
            print('Uploading new user in database: \n' + str(new_user_dict))
            table.put_item(Item=new_user_dict)

            session.clear()
            session['user_in_session'] = new_user_dict
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")