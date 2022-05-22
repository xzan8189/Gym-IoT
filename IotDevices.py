import json
import random

import boto3
# Descrizione di alcuni parametri utilizzati nel codice
# 'arbitraty_value': varrà 6 <- (15min/100cal). è un valore arbitrario e serve solo per simulare le calorie perse
# immaginando che in 15 min perdi circa 100cal utilizzando la stessa forza in maniera costante


def build_msgBody(username: str) -> str:
    time_spent = []
    calories_spent = []

    # aggiungo il Tempo speso su ogni macchina
    for i in range(4):
        value = int(random.randint(0, 60)) # su ogni macchina ci sto massimo 60 minuti
        time_spent.append(str(value))

    # aggiungo le Calorie spese su ogni macchina
    sum = 0
    for item in time_spent:
        value = int(item) * 6
        sum += value
        calories_spent.append(str(value)) #moltiplico per 6 per calcolarmi le calorie perse in base alla quantità di tempo spesa.
        #ovviamente 6 è un valore arbitrario e serve solo per simulare un minimo la realtà

    print("Calories lost in total: " + str(sum))

    msg_body = '{"username": "' + username + '", "time_spent": ' + str(time_spent) + ', "calories_spent": ' + str(calories_spent) + '}'
    msg_body = msg_body.replace("'", '"')

    return msg_body

def build_msgBody2(username: str) -> str:
    value_time_spent = int(random.randint(0, 60)) # su ogni macchina ci sto massimo 60 minuti
    #value_time_spent = "" # serve per la coda 'Errors'
    value_calories_spent = value_time_spent * 6 #moltiplico per 6 per calcolarmi le calorie perse in base alla quantità di tempo spesa.
        #ovviamente 6 è un valore arbitrario e serve solo per simulare un minimo la realtà

    print("Calories lost on machine: " + str(value_calories_spent))

    msg_body = '{"username": "' + username + '", "value_time_spent": "' + str(value_time_spent) + '", "value_calories_spent": "' + str(value_calories_spent) + '"}'
    msg_body = msg_body.replace("'", '"')

    return msg_body

client = boto3.client('sqs', endpoint_url='http://localhost:4566')

if __name__ == '__main__':
    # Creation for queues
    machines = ["Cyclette", "Tapis roulant", "Elliptical bike", "Spin bike"]
    # for machine in machines:
    #     response = client.create_queue( # Creo Queue per ogni macchina della gym
    #         QueueName = machine
    #     )
    # response = client.create_queue( # Creo Queue degli errori
    #     QueueName="Errors"
    # )

    response = client.list_queues(QueueNamePrefix="")
    print('QueueUrls: \n' + str(response["QueueUrls"]) + '\n')

    # Dati da inserire nel msg_body e successivamente da inviare nella Queue
    username = "prova"
    msg_body = build_msgBody2(username=username)

    randomQueue = machines[random.randint(0, 3)]
    response = client.send_message(
        QueueUrl='http://localhost:4566/000000000000/' + randomQueue,
        MessageBody=msg_body # il tipo del messaggio da inviare deve essere di tipo stringa
    )

    # response = client.send_message(
    #     QueueUrl='http://localhost:4566/000000000000/Errors',
    #     MessageBody='{"device_id": "test_error","error_date": "test"}' # il tipo del messaggio da inviare deve essere di tipo stringa
    # )

    # ---------------- RICEZIONE MESSAGGI --------------
    # response = client.receive_message(
    #     QueueUrl='http://localhost:4566/000000000000/' + machines[0]
    # )
    #
    # if 'Messages' in response:
    #     for item in response['Messages']:
    #         #print("item['Body']: " + item['Body'])
    #         body = json.loads(item['Body'])
    #         print("item['Body']: " + str(body))
    #
    #         response = client.delete_message(
    #             QueueUrl='http://localhost:4566/000000000000/' + machines[0],
    #             ReceiptHandle=item['ReceiptHandle']
    #         )


    #---------------- FINALE --------------
    # for machine in machines:
    #     client.delete_queue(
    #         QueueUrl='http://localhost:4566/000000000000/' + machine
    #     )
    # client.delete_queue(
    #     QueueUrl='http://localhost:4566/000000000000/Errors'
    # )
