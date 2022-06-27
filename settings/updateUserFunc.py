import datetime
import json

import boto3
import requests
from botocore.exceptions import ClientError

def reset_donut_and_bar_chart(user):
    time_spent = user['gym']['machines']['time_spent']
    calories_spent = user['gym']['machines']['calories_spent']

    for i in range(len(time_spent)): # reset time_spent
        time_spent[i] = "0"

    for i in range(len(calories_spent)): # reset calories_spent
        calories_spent[i] = "0"

    user['gym']['data']['calories_lost_today'] = "0" # reset calories_lost_today

def calculate_calorie_deficit(sex: str, weight: float, height: float, age: int) -> float:
    if (sex == 'F'):
        return (10 * weight) + (6.25 * height) - (5 * age) - 161
    elif (sex == 'M'):
        return (10 * weight) + (6.25 * height) - (5 * age) + 5

def updateUser(user, msg_body, machine):
    username = msg_body['username']
    value_time_spent = int(msg_body['value_time_spent'])
    value_calories_spent = int(msg_body['value_calories_spent'])

    # update field 'last_time_user_was_updated'. I need this information to understand when i must to restart the donut and bar chat
    date_format = '%Y-%m-%d'
    a = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), date_format)
    b = datetime.datetime.strptime(user['last_time_user_was_updated'], date_format)
    delta = a - b
    if delta.days != 0:
        reset_donut_and_bar_chart(user=user)
        user['last_time_user_was_updated'] = datetime.datetime.today().strftime('%Y-%m-%d')
    print("Days: " + str(delta.days))

    # I DON'T UPDATE FIELD '['info']['weight']' EVERYDAY: because if you update it everyday
    # then it will be changed everyday the value 'monthly_target_percentage' passed from view.home, but we don't want this.
    # We want that the 'weight' is going to be updated only at the end of the month
    # --------------------------- DEVI RIMUOVERE QUESTO CODICE PERCHé NON è UTILE! -----------------
    # now = datetime.datetime.now()
    # if int(user['gym']['calories'][str(now.year)][now.month-1]) == 0: # it's a new month, so i update the weight
    #     user['info']['weight'] = str(float(user['info']['weight']) - float(user['gym']['data']['calories_lost'])) # updating weight
    #     user['gym']['data']['calories_to_reach_today'] = str(calculate_calorie_deficit(user['info']['sex'], float(user['info']['weight']), float(user['info']['height']), int(user['info']['age']))) # updating the "calorie deficit"

    # update fields 'data'
    user['gym']['data']['calories_lost'] = str(int(user['gym']['data']['calories_lost']) + value_calories_spent)
    user['gym']['data']['calories_lost_today'] = str(int(user['gym']['data']['calories_lost_today']) + value_calories_spent)

    # update fields 'machines'
    index_machine = list(user['gym']['machines']['name_machine']).index(machine)
    user['gym']['machines']['time_spent'][index_machine] = str(int(user['gym']['machines']['time_spent'][index_machine]) + value_time_spent)
    user['gym']['machines']['calories_spent'][index_machine] = str(int(user['gym']['machines']['calories_spent'][index_machine]) + value_calories_spent)

    # update fields 'calories'
    now = datetime.datetime.now()
    user['gym']['calories'][str(now.year)][now.month-1] = str(int(user['gym']['calories'][str(now.year)][now.month-1]) + value_calories_spent)

    return user


def lambda_handler(event, context):
    client = boto3.client('sqs', endpoint_url='http://localhost:4566')
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    table = dynamodb.Table('Users')

    machines = ["Cyclette", "Tapis_roulant", "Elliptical_bike", "Spin_bike"]

    #while True:
    for machine in machines:
        response = client.receive_message(
            QueueUrl='http://localhost:4566/000000000000/' + machine
        )
        if 'Messages' in response:
            for item in response['Messages']:
                msg_body = json.loads(item['Body'])
                print("Queue: " + machine + ",\nitem['Body']: " + str(msg_body))

                try:
                    response = table.get_item(Key={'username': msg_body['username']}) # Getting user from database
                    if 'Item' in response:
                        user = response['Item']
                        print(user)

                        # Check parameter's message. If they are not correct I send an error message to Errors queue
                        if ('username' not in msg_body or msg_body['username'] == "") or ('value_time_spent' not in msg_body or msg_body['value_time_spent'] == "") or ('value_calories_spent' not in msg_body or msg_body['value_calories_spent'] == ""):
                            print("ERROR")
                            username = "ERROR" if ('username' not in msg_body or msg_body['username'] == "") else msg_body['username']
                            value_time_spent = "ERROR" if ('value_time_spent' not in msg_body or msg_body['value_time_spent'] == "") else msg_body['value_time_spent']
                            value_calories_spent = "ERROR" if ('value_calories_spent' not in msg_body or msg_body['value_calories_spent'] == "") else msg_body['value_calories_spent']

                            msg_error_body = '{"device_id": "' + str(machine) + '", "value_time_spent": "' + str(value_time_spent) + '", "value_calories_spent": "' + str(value_calories_spent)+ '"}'
                            print("\n\nmsg_error_body: " + msg_error_body)
                            response = client.send_message(
                                QueueUrl='http://localhost:4566/000000000000/Errors',
                                MessageBody=msg_error_body
                            )
                        else: # Parameters are good, so I can proceed with the update of user
                            user = updateUser(user=user, msg_body=msg_body, machine=machine)
                            table.put_item(Item=user)
                            requests.post('http://127.0.0.1:5000/listen',json={'username': user['username']})
                    else:
                        print('User "' + msg_body['username'] + '" not found!')

                except ClientError as e:
                    print(e.response['Error']['Message'])
                print()

                response = client.delete_message( # Delete message from queue
                    QueueUrl='http://localhost:4566/000000000000/' + machine,
                    ReceiptHandle=item['ReceiptHandle']
                )

# if __name__ == '__main__':
#     lambda_handler(None, None)