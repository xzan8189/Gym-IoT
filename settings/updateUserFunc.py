import json

import boto3


def lambda_handler(event, context):
    client = boto3.client('sqs', endpoint_url='http://localhost:4566')
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
    table = dynamodb.Table('Users')

    machines = ["Cyclette", "Tapis roulant", "Elliptical bike", "Spin bike"]

    while True:
        for machine in machines:
            response = client.receive_message(
                QueueUrl='http://localhost:4566/000000000000/' + machine
            )
            if 'Messages' in response:
                for item in response['Messages']:
                    #print("item['Body']: " + item['Body'])
                    body = json.loads(item['Body'])
                    print("Queue: " + machine + ",\nitem['Body']: " + str(body))

                    response = client.delete_message(
                        QueueUrl='http://localhost:4566/000000000000/' + machine,
                        ReceiptHandle=item['ReceiptHandle']
                    )

if __name__ == '__main__':
    lambda_handler(None, None)