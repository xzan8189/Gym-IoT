import boto3
import json
import requests
from settings.config import DefaultConfig

CONFIG = DefaultConfig()

def machines_and_exercises_left(training_card_updated, machine_or_exercise_done):
    username = training_card_updated['id']
    schedule = training_card_updated['content']['schedule']
    calories_or_repetitions = training_card_updated['content']['calories_or_repetitions']
    msg_machines_and_exercises_left = f"{username}, la volevamo informare che non sta seguendo correttamente la scheda di allenamento!\n\n*🚴‍♂️Gli esercizi da fare sono questi: *\n"


    i = 0
    flag = 0
    for item in calories_or_repetitions:
        if schedule[i] == machine_or_exercise_done:
            break
        elif int(item) > 0:
            flag = 1
            msg_machines_and_exercises_left += str(schedule[i]).replace("_", " ") + "\n"
        i = i+1

    if flag == 1: # Sending message
        print(f"Message: {msg_machines_and_exercises_left}\nSending message...")
        requests.get('https://api.telegram.org/bot' + CONFIG.BOT_TOKEN + '/sendMessage?chat_id=' + CONFIG.BOT_CHAT_ID + '&parse_mode=Markdown&text=' + msg_machines_and_exercises_left)

def updateTrainingCardUser(training_card, msg_body):
    username = msg_body['username']
    machine_or_exercise = msg_body['machine_or_exercise']
    value_calories_spent = int(msg_body['value_calories_spent'])

    if machine_or_exercise not in training_card['content']['schedule']: # The machine is not inside the training card. EXIT.
        print(f"The {machine_or_exercise} is not inside training card of user\n")
        return False

    index_machine = list(training_card['content']['schedule']).index(machine_or_exercise)

    value = int(training_card['content']['calories_or_repetitions'][index_machine]) - value_calories_spent
    print(str(training_card['content']['calories_or_repetitions'][index_machine]) + " - " + str(value_calories_spent) + " = " + str(value))
    if type(training_card['content']['calories_or_repetitions'][index_machine]) is str: # Check if it is a string. CALORIES.
        print("it's a STRING")
        if (value < 0):
            training_card['content']['calories_or_repetitions'][index_machine] = "0"
        else:
            training_card['content']['calories_or_repetitions'][index_machine] = str(int(training_card['content']['calories_or_repetitions'][index_machine]) - value_calories_spent)

    else: # It is not a string, so it's an int. REPETITIONS.
        print("it's a INT")
        if (value < 0):
            training_card['content']['calories_or_repetitions'][index_machine] = 0
        else:
            training_card['content']['calories_or_repetitions'][index_machine] = int(training_card['content']['calories_or_repetitions'][index_machine]) - value_calories_spent

    print(str(training_card) + "\n")
    return training_card

def lambda_handler(event, context):
    client = boto3.client('sqs', endpoint_url='http://localhost:4566')
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    table = dynamodb.Table('Training_cards')

    while True:
        response = client.receive_message(
            QueueUrl='http://localhost:4566/000000000000/Training_card'
        )
        if 'Messages' in response:
            for attribute in response['Messages']:
                msg_body = json.loads(attribute['Body'])
                print("Item['Body']: " + str(msg_body))

                response = table.get_item(Key={'id': msg_body['username']})  # Getting training card of user from database
                if 'Item' in response:
                    training_card = response['Item']
                    training_card_updated = updateTrainingCardUser(training_card, msg_body)
                    client.delete_message(  # Delete message from queue
                        QueueUrl='http://localhost:4566/000000000000/Training_card',
                        ReceiptHandle=attribute['ReceiptHandle']
                    )
                    if training_card_updated == False:
                        break

                    table.put_item(Item=training_card_updated)

                    index_machine = list(training_card_updated['content']['schedule']).index(msg_body['machine_or_exercise'])
                    calories_or_repetitions_spent = training_card_updated['content']['calories_or_repetitions'][index_machine]
                    if type(calories_or_repetitions_spent) is str:
                        calories_or_repetitions_spent = str(calories_or_repetitions_spent)
                    requests.post('http://127.0.0.1:5000/listenTrainingCard', # Updating website
                                  json={
                                      'username': msg_body['username'],
                                      'machine_or_exercise': msg_body['machine_or_exercise'],
                                      'calories_or_repetitions_spent': calories_or_repetitions_spent
                                  })
                    machines_and_exercises_left(training_card_updated, msg_body['machine_or_exercise']) # Notify via Telegram if the customer is not performing the correct execution of the training card

if __name__ == '__main__':
    lambda_handler(None, None)