from decimal import Decimal
import json
import boto3
from botocore.exceptions import ClientError
from models.User import User

# Variabili d'istanza
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Users')

# Metodi della classe
def load_users(users):
    for customer in users['Users']:
        user = User(customer['username'], customer['name'], customer['surname'], customer['password'], customer['registration_date'])
        #print(f"Adding user: \n{user}")
        table.put_item(Item=customer)

if __name__ == '__main__':
    with open("userdata.json") as json_file:
        user_list = json.load(json_file, parse_float=Decimal)

    load_users(user_list)
    username = input("Scrivi l'username dell'utente da trovate nel DB: ")

    try:
        response = table.get_item(Key={'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])

    user_found = User(response['Item']['username'], response['Item']['name'], response['Item']['surname'], response['Item']['password'], response['Item']['registration_date'])
    print(f"L'utente è stato trovato: \n{user_found}")