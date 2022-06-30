from datetime import datetime

import boto3
import flask
from botocore.exceptions import ClientError
from flask import Blueprint, render_template, flash, session, url_for, request, Response
from werkzeug.utils import redirect

from models.Utils import Utils

views = Blueprint('views', __name__)

# Variabili d'istanza
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table_users = dynamodb.Table('Users')
table_training_cards = dynamodb.Table('Training_cards')

@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_in_session' not in session: # No user in session, he tried to go in "home.html" without login before
        flash('You must log-in before!', category='error')
        return redirect(url_for('auth.login'))
    else: # User in session, so now he can go in "home.html"
        try:
            username = session['user_in_session']['username']
            user_found_dict = table_users.get_item(Key={'username': username})
            if len(user_found_dict) > 1:
                training_card_found_dict = table_training_cards.get_item(Key={'id': user_found_dict['Item']['training_card_info']['training_card_id']})
                if len(training_card_found_dict) > 1:
                    print(training_card_found_dict['Item'])
                    session['user_in_session'] = user_found_dict['Item']
                    session['training_card_in_session'] = training_card_found_dict['Item']

                    return render_template("home.html", user=user_found_dict['Item'], training_card=training_card_found_dict['Item'],
                                           monthly_target_percentage=Utils.calculate_monthly_target_percentage(user_found_dict['Item']),
                                           current_date=str(datetime.today().strftime('%B %d, %Y')))
            else:
                flash('Username does not exist.', category='error')
                return render_template("login.html")

        except ClientError as e:
            print(e.response['Error']['Message'])

@views.route('/training_card', methods=['GET', 'POST'])
def training_card():
    if 'user_in_session' not in session: # No user in session, he tried to go in "home.html" without login before
        flash('You must log-in before!', category='error')
        return redirect(url_for('auth.login'))
    else: # User in session, so now he can go in "training_card.html"
        try:
            username = session['user_in_session']['username']
            user_found_dict = table_users.get_item(Key={'username': username})
            if len(user_found_dict) > 1:
                training_card_found_dict = table_training_cards.get_item(Key={'id': user_found_dict['Item']['training_card_info']['training_card_id']})
                if len(training_card_found_dict) > 1:
                    print(training_card_found_dict['Item'])
                    session['user_in_session'] = user_found_dict['Item']
                    session['training_card_in_session'] = training_card_found_dict['Item']

                    return render_template("training_card.html", user=user_found_dict['Item'], training_card=training_card_found_dict['Item'])
            else:
                flash('Username does not exist.', category='error')
                return render_template("login.html")

        except ClientError as e:
            print(e.response['Error']['Message'])

flag = False
data_json = "nothing"
@views.route("/listen", methods=['GET', 'POST'])
def listen():
    global flag, data_json
    if request.method == 'POST': # Receive data
        flag = True
        data_json = flask.request.json

    def respond_to_client(): # Sending data to event
        user_found_dict = table_users.get_item(Key={'username': data_json['username']})
        yield f"data: {user_found_dict['Item']}\nevent: {data_json['username']}\n\n"

    if request.method == 'GET' and flag: # Send data
        flag=False
        return Response(respond_to_client(), mimetype='text/event-stream')

    return Response(mimetype='text/event-stream') # There is nothing. I have to return something otherwise it will give an error the eventListener in Javascript