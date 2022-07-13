import requests

import boto3

from settings.config import DefaultConfig

CONFIG = DefaultConfig()

def send_email_to_customer(username, event):
    client = boto3.client('ses', endpoint_url="http://localhost:4566")

    payment_amount = event['payment_amount']
    email_customer = event['email_customer']
    data_message = ""

    if int(event['tip_amount']) > 0:
        data_message = f"Thanks {username}!, " \
                       f"Not only you paid for the month (70 euros), but you also gave us a tip worth {event['tip_amount']} euros, we really appreciate it! " \
                       f"We are happy to know that the service provided is appreciated so much." \
                       f"Payment amount: {payment_amount}, Tip amount: {event['tip_amount']}"
    else:
        data_message = f"Thanks {username}!, " \
                       f"We are happy to know that the service provided is appreciated.\n" \
                       f"Payment amount: {payment_amount}"

    message = {
        'Subject': {
            'Data': 'Gym IoT monthly bill',
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
                email_customer,
            ],
            'CcAddresses': [],
            'BccAddresses': []
        },
        Message=message
    )
    print("The message with id '" + response["MessageId"] + "' is corrected sent to " + email_customer)
    return data_message

def lambda_handler(event, context):
    # Data
    username = event['username']
    payment_amount = event['payment_amount']
    tip_amount = event['tip_amount']

    if int(tip_amount) > 0:
        response = {
            'username': username,
            'payment_amount': payment_amount,
            'tip_amount': event['tip_amount']
        }
    else: response = {}

    send_email_to_customer(username, event)
    return response