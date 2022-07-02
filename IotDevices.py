import json
import random

import boto3

def build_msgBody(username: str) -> str:
    value_time_spent = int(random.randint(0, 60)) # I use the machine max 60 min
    #value_time_spent = "" # extract this line (and put the line above between comments) from the comment to send a message to 'Errors' queue
    value_calories_spent = value_time_spent * 6 # I multiply with the number 6 to simulate the calories_spent on the machine

    print("Calories lost on machine: " + str(value_calories_spent))

    msg_body = '{"username": "' + username + '", "value_time_spent": "' + str(value_time_spent) + '", "value_calories_spent": "' + str(value_calories_spent) + '"}'
    msg_body = msg_body.replace("'", '"')

    return msg_body

client = boto3.client('sqs', endpoint_url='http://localhost:4566')

if __name__ == '__main__':
    # Creating Queues
    machines = ["Cyclette", "Tapis_roulant", "Elliptical_bike", "Spin_bike"]
    for machine in machines:
        response = client.create_queue( # Creating Queue for each machine of gym
            QueueName = machine
        )
    response = client.create_queue( # Creating Training_card Queue
        QueueName="Training_card"
    )
    response = client.create_queue( # Creating Error Queue
        QueueName="Errors"
    )

    response = client.list_queues(QueueNamePrefix="")
    print('QueueUrls: \n' + str(response["QueueUrls"]) + '\n')

    # Creating message to send to Queue
    username = "xzan8189"
    msg_body = build_msgBody(username=username)

    randomQueue = machines[random.randint(0, 3)]
    response = client.send_message( # Sending message to Queue
        QueueUrl='http://localhost:4566/000000000000/' + randomQueue,
        MessageBody=msg_body
    )

    # ---------------- END - Deleting Queues --------------
    # for machine in machines:
    #     client.delete_queue(
    #         QueueUrl='http://localhost:4566/000000000000/' + machine
    #     )
    # client.delete_queue(
    #     QueueUrl='http://localhost:4566/000000000000/Errors'
    # )
    # client.delete_queue(
    #     QueueUrl='http://localhost:4566/000000000000/Training_card'
    # )
