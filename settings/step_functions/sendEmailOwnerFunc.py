import boto3
import requests

from settings.config import DefaultConfig

CONFIG = DefaultConfig()

def send_email_to_owner(username, event):
    client = boto3.client('ses', endpoint_url="http://localhost:4566")

    payment_amount = event['payment_amount']
    data_message = ""

    data_message = f"Hi Owner, We wanted to inform you that the user '{username}' gave a tip of {str(int(payment_amount)- 70)} euros! " \
                   f"Payment amount: {payment_amount}, Tip amount: {event['tip_amount']}"

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
    response = client.send_email(
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
    return data_message

def lambda_handler(event, context):
    send_email_to_owner(event['username'], event)