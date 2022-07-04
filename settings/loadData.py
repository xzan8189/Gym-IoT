import datetime
from decimal import Decimal
import json
import boto3
from botocore.exceptions import ClientError
from models.User import User

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Users')

def load_users(users):
    for customer in users['Users']:
        #print(f"Adding user: \n{user}")
        table.put_item(Item=customer)

if __name__ == '__main__':
    with open("settings/userdata.json") as json_file:
        user_list = json.load(json_file, parse_float=Decimal)

    load_users(user_list)
    #username = input("Write the username of the customer to find: ")
    username = "xzan8189"

    try:
        response = table.get_item(Key={'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])

    user_found = User(
            username=response['Item']['username'],
            name=response['Item']['name'],
            surname=response['Item']['surname'],
            password=response['Item']['password'],
            registration_date=response['Item']['registration_date'],
            last_time_user_was_updated=response['Item']['last_time_user_was_updated'],
            sex=response['Item']['info']['sex'],
            age=response['Item']['info']['age'],
            weight=response['Item']['info']['weight'],
            height=response['Item']['info']['height'],
            calories_to_reach_today=response['Item']['gym']['data']['calories_to_reach_today']
        )

    for item in response['Item']['gym']['calories'].items():
        print(item[0] + ": " + str(item[1]))
