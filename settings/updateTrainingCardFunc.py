import json

import boto3
import requests

from settings.config import DefaultConfig

CONFIG = DefaultConfig()

def machines_and_exercises_left(training_card_updated, machine_or_exercise_done, user):
    username = training_card_updated['id']
    schedule = training_card_updated['content']['schedule']
    calories_or_repetitions = training_card_updated['content']['calories_or_repetitions']
    msg_machines_and_exercises_left = f"🚨 Hi {username}, We wanted to inform you that you are not following the training schedule correctly!\n\n" \
                                      f"⚠ You are currently using this machine: *{str(machine_or_exercise_done).replace('_', ' ')}*\n\n" \
                                      f"*But you have some exercise to finish yet ⤵️*\n"

    i = 0
    flag = 0
    for item in calories_or_repetitions:
        if schedule[i] == machine_or_exercise_done:
            break
        elif int(item) > 0:
            flag = 1
            msg_machines_and_exercises_left += str(schedule[i]).replace("_", " ") + ": _"
            if type(calories_or_repetitions[i]) is str:
                msg_machines_and_exercises_left += str(calories_or_repetitions[i]) + " Cal_\n"
            else:
                msg_machines_and_exercises_left += str(calories_or_repetitions[i]) + " Rep_\n"
        i = i+1

    if flag == 1 and user['telegram_chat_id'] != "": # Sending message
        print(f"Message: {msg_machines_and_exercises_left}\nSending message...\n")
        requests.get('https://api.telegram.org/bot' + CONFIG.BOT_TOKEN + '/sendMessage?chat_id=' + user['telegram_chat_id'] + '&parse_mode=Markdown&text=' + msg_machines_and_exercises_left)

def updateTrainingCardUser(training_card, msg_body):
    username = msg_body['username']
    machine = msg_body['machine_or_exercise']
    value_calories_spent = int(msg_body['value_calories_spent'])

    if machine not in training_card['content']['schedule']: # The machine is not inside the training card. EXIT.
        print(f"The {machine} is not inside training card of user\n")
        return False

    index_machine = list(training_card['content']['schedule']).index(machine)
    value = int(training_card['content']['calories_or_repetitions'][index_machine]) - value_calories_spent
    print(str(training_card['content']['calories_or_repetitions'][index_machine]) + " - " + str(value_calories_spent) + " = " + str(value))
    if (value < 0):
        training_card['content']['calories_or_repetitions'][index_machine] = "0"
    else:
        training_card['content']['calories_or_repetitions'][index_machine] = str(int(training_card['content']['calories_or_repetitions'][index_machine]) - value_calories_spent)

    training_card['machine_just_done']['name_machine'] = machine
    training_card['machine_just_done']['calories_consumed'] = value_calories_spent

    print(str(training_card) + "\n")
    return training_card

def lambda_handler(event, context):
    client = boto3.client('sqs', endpoint_url='http://localhost:4566')
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    table_users = dynamodb.Table('Users')
    table_training_cards = dynamodb.Table('Training_cards')

    #while True:
    response = client.receive_message(
        QueueUrl='http://localhost:4566/000000000000/Training_card'
    )
    if 'Messages' in response:
        for attribute in response['Messages']:
            msg_body = json.loads(attribute['Body'])
            print("Item['Body']: " + str(msg_body))

            response = table_training_cards.get_item(Key={'id': msg_body['username']})  # Getting training card of user from database
            if 'Item' in response:
                training_card = response['Item']
                training_card_updated = updateTrainingCardUser(training_card, msg_body)
                client.delete_message(  # Delete message from queue
                    QueueUrl='http://localhost:4566/000000000000/Training_card',
                    ReceiptHandle=attribute['ReceiptHandle']
                )
                if training_card_updated == False:
                    break

                table_training_cards.put_item(Item=training_card_updated)
                user = table_users.get_item(Key={'username': msg_body['username']})
                machines_and_exercises_left(training_card_updated, msg_body['machine_or_exercise'], user['Item']) # Notify via Telegram if the customer is not performing the correct execution of the training card

# if __name__ == '__main__':
#     lambda_handler(None, None)