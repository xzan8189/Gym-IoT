import json
import random

import boto3
# Descrizione di alcuni parametri utilizzati nel codice
# 'arbitraty_value': varrà 6 <- (15min/100cal). è un valore arbitrario e serve solo per simulare le calorie perse
# immaginando che in 15 min perdi circa 100cal utilizzando la stessa forza in maniera costante


def build_msgBody(username: str) -> str:
    time_spent = []
    calories_spent = []

    for i in range(4):
        minutes = 60
        arbitraty_value = 6
        value = int(random.randint(0, 800) / minutes * arbitraty_value)
        time_spent.append(str(value))

    for item in time_spent:
        calories_spent.append(str(int(item) * 6)) #moltiplico per 6 per calcolarmi le calorie perse in base alla quantità di tempo spesa.
        #ovviamente 6 è un valore arbitrario e serve solo per simulare un minimo la realtà

    msg_body = '{"username": "' + username + '", "time_spent": ' + str(time_spent) + ', "calories_spent": ' + str(
        calories_spent) + '}'
    msg_body = msg_body.replace("'", '"')

    return msg_body


client = boto3.client('sqs', endpoint_url='http://localhost:4566')

if __name__ == '__main__':
    # response = client.create_queue(
    #     QueueName = 'gym_queue'
    # )

    response = client.list_queues(QueueNamePrefix="")
    print(response["QueueUrls"])

    # Dati da inserire nel msg_body e successivamente da inviare nella Queue
    username = "xzan8189"
    #time_spent = ['25', '35', '60', '40']
    #calories_spent = ['100', '140', '220', '150'] non serve più, perché lo calcoli nella funzione 'build_msgBody'
    # msg_body = '{"username": "%s","time_spent": %s,"calories_spent": %s}' % (username, str(time_spent), str(calories_spent))
    # print(msg_body)
    msg_body = build_msgBody(username=username)

    response = client.send_message(
        QueueUrl='http://localhost:4566/000000000000/gym_queue',
        MessageBody=msg_body # il tipo del messaggio da inviare deve essere di tipo stringa
    )

    response = client.receive_message(
        QueueUrl='http://localhost:4566/000000000000/gym_queue'
    )

    for item in response['Messages']:
        #print("item['Body']: " + item['Body'])
        body = json.loads(item['Body'])
        print("item['Body']: " + str(body))

    response = client.delete_message(
        QueueUrl='http://localhost:4566/000000000000/gym_queue',
        ReceiptHandle=item['ReceiptHandle']
    )

    # client.delete_queue(
    #     QueueUrl='http://localhost:4566/000000000000/gym_queue'
    # )
