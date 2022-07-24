from datetime import datetime

import boto3
import flask
from botocore.exceptions import ClientError
from flask import Blueprint, render_template, flash, session, url_for, request, Response
from werkzeug.utils import redirect

from models.Utils import Utils

views = Blueprint('views', __name__)

# Instance variables
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
                #print(username)
                training_card_found_dict = table_training_cards.get_item(Key={'id': username})
                if len(training_card_found_dict) > 1:
                    #print(training_card_found_dict['Item'])
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
                training_card_found_dict = table_training_cards.get_item(Key={'id': username})
                if len(training_card_found_dict) > 1:
                    #print(training_card_found_dict['Item'])
                    session['user_in_session'] = user_found_dict['Item']
                    session['training_card_in_session'] = training_card_found_dict['Item']

                    return render_template("training_card.html", user=user_found_dict['Item'], training_card=training_card_found_dict['Item'])
            else:
                flash('Username does not exist.', category='error')
                return render_template("login.html")

        except ClientError as e:
            print(e.response['Error']['Message'])

@views.route('/insert_repetitions', methods=['GET', 'POST'])
def insert_repetitions():
    name_exercise = request.form.get('name_exercise')
    num_repetitions = int(request.form.get('num_repetitions'))

    username = session['user_in_session']['username']
    training_card_found_dict = table_training_cards.get_item(Key={'id': username})
    if len(training_card_found_dict) > 1:
        training_card_found_dict = training_card_found_dict['Item']
        index_exercise = list(training_card_found_dict['content']['schedule']).index(name_exercise)
        current_repetitions = training_card_found_dict['content']['calories_or_repetitions'][index_exercise]
        current_repetitions = int(current_repetitions) - num_repetitions
        if current_repetitions < 0:
            current_repetitions = 0

        training_card_found_dict['content']['calories_or_repetitions'][index_exercise] = current_repetitions
        table_training_cards.put_item(Item=training_card_found_dict) # Updating training_card
        flash(f'Updated {name_exercise} exercise, you did about {num_repetitions} Reps!', category='success')

    return redirect(url_for('views.training_card'))


@views.route("/listen", methods=['GET', 'POST'])
def listen():
    flag = False
    username = session['user_in_session']['username']
    user_found_dict = table_users.get_item(Key={'username': username})['Item']

    if user_found_dict['modified'] == True: # User modified, we need to refresh the data in the page
        flag = True

    def respond_to_client(): # Sending data to event
        yield f"data: {user_found_dict}\nevent: {username}\n\n"

    if request.method == 'GET' and flag: # Send data
        flag=False
        user_found_dict['modified'] = False
        table_users.put_item(Item=user_found_dict)
        return Response(respond_to_client(), mimetype='text/event-stream')

    return Response(mimetype='text/event-stream') # There is nothing. I have to return something otherwise it will give an error the eventListener in Javascript

@views.route("/listenTrainingCard", methods=['GET', 'POST'])
def listenTrainingCard():
    flag = False
    username = session['user_in_session']['username']
    trainingCard_found_dict = table_training_cards.get_item(Key={'id': username})['Item']

    if trainingCard_found_dict['machine_just_done']['name_machine'] != "": # Trainining card modified, we need to refresh the data in the page
        flag = True

    def respond_to_client(): # Sending data to event
        trainingCard_found_dict = table_training_cards.get_item(Key={'id': username})['Item']
        name_machine = trainingCard_found_dict['machine_just_done']['name_machine']
        calories_consumed = trainingCard_found_dict['machine_just_done']['calories_consumed']

        index_machine = list(trainingCard_found_dict['content']['schedule']).index(name_machine)
        calories_left = trainingCard_found_dict['content']['calories_or_repetitions'][index_machine]
        data = {
            "name_machine": name_machine,
            "calories_consumed": calories_consumed,
            "calories_left": calories_left
        }

        print(f"username: {username}, name_machine: {name_machine}, calories_consumed: {calories_consumed}")

        trainingCard_found_dict['machine_just_done']['name_machine'] = ""
        table_training_cards.put_item(Item=trainingCard_found_dict)

        yield f"data: {data}\nevent: {username}TrainingCard\n\n"

    if request.method == 'GET' and flag: # Send data
        flag=False
        return Response(respond_to_client(), mimetype='text/event-stream')

    return Response(mimetype='text/event-stream') # There is nothing. I have to return something otherwise it will give an error the eventListener in Javascript
