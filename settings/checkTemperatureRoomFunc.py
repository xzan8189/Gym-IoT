import boto3
import requests
from boto3.dynamodb.conditions import Attr


def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] != "REMOVE": # We want to process only 'INSERT' and 'MODIFY' events
            newImage = record['dynamodb']['NewImage']

            # Data
            id = newImage['id']['N']
            temperature = newImage['temperature']['N']
            name_room = newImage['name_room']['S']
            air_conditioner = newImage['air_conditioner']['BOOL']

            if int(temperature) >= 30:
                dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
                table_users = dynamodb.Table('Users')

                # Scanning table to find users that are training in that gym room
                response = table_users.scan(
                    FilterExpression=Attr("gym_room").eq(int(id))
                )

                for item in response['Items']:
                    if item['telegram_chat_id'] != "": # Only to the customers that have Telegram I send the message (on Telegram)
                        requests.get('https://api.telegram.org/bot' + "5364582485:AAH-7yk83uU3BRAvWGuZWtujcYhwsVHeziw" + '/sendMessage?chat_id=' + item['telegram_chat_id'] +
                                     '&parse_mode=Markdown&text=' +
                                     f"🌡Hi {item['username']}, it was detected in *{name_room}* a temperature of *{str(temperature)}°*, it is quite high!\n\n"
                                     f"❄️It will be activated the air conditioner to lower the temperature, till to arrive *25°*\n\n"
                                     f"🧍‍♂️If you have any problem talk with a manager of the infrastracture!")