import requests
import boto3
import datetime
import json

from settings.config import DefaultConfig

CONFIG = DefaultConfig()


def lambda_handler(event, context):
    for record in event['Records']:
        body = record['body']
        body = json.loads(str(body))

        # Data to send
        device_id = body['device_id']
        value_time_spent = body['value_time_spent']
        value_calories_spent = body['value_calories_spent']

        client_sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
        client_ses = boto3.client('ses', endpoint_url="http://localhost:4566")
        data_message = f"<b>Device_id</b>: {str(device_id)}<br>" \
                       f"<b>When</b>: {str(datetime.datetime.now())}<br>" \
                       f"<b>Extra Data</b>:<br>" \
                       f"value_time_spent: {str(value_time_spent)},<br>" \
                       f"value_calories_spent: {str(value_calories_spent)}"

        message = {
            'Subject': {
                'Data': 'Gym IoT Tip Received',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': data_message,
                    'Charset': 'UTF-8'
                },
                'Html': {
                    'Data': 'This message body contains HTML formatting.',
                    'Charset': 'UTF-8'
                }
            }
        }

        source = CONFIG.EMAIL_OWNER
        response = client_ses.send_email(
            Source=source,
            Destination={
                'ToAddresses': [
                    source,
                ],
                'CcAddresses': [],
                'BccAddresses': []
            },
            Message=message
        )
        print("The message with id '" + response["MessageId"] + "' is corrected sent to " + source)

        response = client_sqs.delete_message(  # Delete message from queue
            QueueUrl='http://localhost:4566/000000000000/Errors',
            ReceiptHandle=record['receiptHandle']
        )
