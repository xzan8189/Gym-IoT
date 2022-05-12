import time

import boto3
import datetime
import random
import json


# Variabili d'istanza
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Users')

sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

# Dati da inviare nella queue
username = "xzan8189"
time_spent = ['25', '35', '60', '40']
calories_spent = ['100', '140', '220', '150']

# Dopo fai una prova con questi array
# time_spent = ["0", "35", "0", "40"]
# calories_spent = ["0", "140", "0", "150"]

# Dopo fai un'altra prova mandando un unico oggetto json, ma con array di più persone
#for time_item, calories_item in zip(time_spent, calories_spent):
#print(f'Caricando -> Time: {time_item}, Calories: {calories_item}')

queue = sqs.get_queue_by_name(QueueName= "gym_queue")
msg_body = '{"time_spent": ' + str(time_spent) + '," calories_spent": ' + str(calories_spent) + '}'
msg_body = msg_body.replace("'", '"')
#content = json.loads(msg_body)
print("Caricato msg_body: " + msg_body)
queue.send_message(MessageBody=msg_body)

messages = []
while True:
	response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
	if response:
		messages.extend(response)
		for message in messages:
			content = json.loads(str(message.body))
			print("Ricevuto: " + str(content))
			message.delete()
	else:
		break
