import time
from datetime import datetime

import boto3
import flask
from botocore.exceptions import ClientError
from flask import Blueprint, render_template, flash, jsonify, session, url_for, request, Response, \
    copy_current_request_context
from flask_sse import sse
from werkzeug.utils import redirect

from models.Utils import Utils

views = Blueprint('views', __name__)

# Variabili d'istanza
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Users')

@views.route('/')
@views.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_in_session' not in session:
        flash('You must log-in before!', category='error')
        return redirect(url_for('auth.login'))
    else: # Serve per quando l'utente ricarica la pagina per vedere i grafici aggiornati (vengono ripresi i dati dell'utente dal database)
        try:
            username = session['user_in_session']['username']
            user_found_dict = table.get_item(Key={'username': username})
            if len(user_found_dict) > 1:
                session['user_in_session'] = user_found_dict['Item']
                return render_template("home.html", user=user_found_dict['Item'],
                                       monthly_target_percentage=Utils.calculate_monthly_target_percentage(user_found_dict['Item']),
                                       current_date=str(datetime.today().strftime('%B %d, %Y')))
            else:
                flash('Username does not exist.', category='error')
                return render_template("login.html")

        except ClientError as e:
            print(e.response['Error']['Message'])


    return render_template("home.html") #non verrà mai raggiunto, poiché tu accedi a questa pagina solo se sei loggato

flag = False
data_json = "nothing"

@views.route("/listen", methods=['GET', 'POST'])
def listen():
    global flag, data_json
    if request.method == 'POST': # Receive data
        flag = True
        data_json = flask.request.json
        print(data_json)

    def respond_to_client(): # Send data to event
        #time.sleep(1)
        print("Invio..")
        yield f"data: {data_json}\nevent: online\n\n"

    if request.method == 'GET' and flag: # Send data
        flag=False
        return Response(respond_to_client(), mimetype='text/event-stream')

    return Response(mimetype='text/event-stream') # There is nothing. I have to return something otherwise it will give an error the eventListener