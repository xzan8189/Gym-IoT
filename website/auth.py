from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, current_user

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
                    user_found_obj = Utils.dictUser_to_object(user_found_dict)
                    session['user_in_session'] = user_found_dict['Item']
                    #return render_template("home.html", user=user_found_dict['Item'])
                    return redirect(url_for('views.home', user=user_found_dict['Item']))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
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
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        surname = request.form.get('surname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')


        #controlli
        try:
            response = table.get_item(Key={'username': username})
            print(response)
        except ClientError as e:
            print(e.response['Error']['Message'])

        if len(username) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif 'Item' in response:
            flash('Email already exists. So the user already exists.', category='error')
        elif len(name) < 2:
            flash("First name must be greater than 2 characters.", category='error')
        elif len(surname) < 2:
            flash("Surname must be greater than 2 characters.", category='error')
        elif password1 != password2:
            flash("Passwords don\'t match.", category='error')
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            #password = generate_password_hash(password1, method='sha256')
            new_user = User(username=username, name=name, surname=surname, password=generate_password_hash(password1, method='sha256'), registration_date=str(datetime.date(datetime.now())))
            print(new_user)
            new_user_dict = Utils.objectUser_to_dict(new_user)
            table.put_item(Item=new_user_dict)

            session.clear()
            session['user_in_session'] = new_user_dict
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")