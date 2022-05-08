import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
import json

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
                user_found_obj = Utils.dictUser_to_object(user_found_dict)
                session['user_in_session'] = user_found_dict['Item']
                return render_template("home.html", user=user_found_dict['Item'])
            else:
                flash('Email does not exist.', category='error')
                return render_template("login.html")

        except ClientError as e:
            print(e.response['Error']['Message'])


    return render_template("home.html")

@views.route('/delete-note', methods=['POST'])
def delete_note():
    return jsonify({})
