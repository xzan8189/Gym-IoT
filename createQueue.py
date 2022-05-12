import json

import boto3
#sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

client = boto3.client('sqs', endpoint_url='http://localhost:4566')

response = client.list_queues(QueueNamePrefix="")

print(response["QueueUrls"])

response = client.send_message(
    QueueUrl='http://localhost:4566/000000000000/gym_queue',
    MessageBody='prova'
)

response = client.receive_message(
    QueueUrl='http://localhost:4566/000000000000/gym_queue'
)

for item in response['Messages']:
    print(item['Body'])


client.delete_queue(
    QueueUrl='http://localhost:4566/000000000000/gym_queue'
)