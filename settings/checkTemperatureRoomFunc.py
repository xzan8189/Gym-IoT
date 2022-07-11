import boto3
import requests
from boto3.dynamodb.conditions import Attr


def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] != "REMOVE": # We want to process only 'INSERT' and 'MODIFY' events
            newImage = record['dynamodb']['NewImage']
            oldImage = record['dynamodb']['OldImage']

            # Data
            id = newImage['id']['N']
            temperature = newImage['temperature']['N']
            name_room = newImage['name_room']['S']
            new_air_conditioner = newImage['air_conditioner']['BOOL']
            old_air_conditioner = oldImage['air_conditioner']['BOOL']

            if int(temperature) >= 30 and old_air_conditioner == False: # Checking also that the air conditioner is off
                dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
                table_users = dynamodb.Table('Users')
                temperature_to_reach = 25

                # Scanning table to find users that are training in that gym room
                response = table_users.scan(
                    FilterExpression=Attr("gym_room").eq(int(id))
                )

                # Send request to the IoT device that enables the air conditioner
                print("requests.get('https://air_conditioner?id=" + str(id) + "&temperature_to_reach=" + str(temperature_to_reach) + "')")

                # Sending message to customers that are training in that room
                for item in response['Items']:
                    if item['telegram_chat_id'] != "": # I send the message only to customers that have Telegram connected (because i send the message on Telegram)
                        requests.get('https://api.telegram.org/bot' + "5364582485:AAH-7yk83uU3BRAvWGuZWtujcYhwsVHeziw" + '/sendMessage?chat_id=' + item['telegram_chat_id'] +
                                     '&parse_mode=Markdown&text=' +
                                     f"🌡Hi {item['username']}, it was detected in *{name_room}* a temperature of *{str(temperature)}°*, it is quite high!\n\n"
                                     f"❄️It will be activated the air conditioner to lower the temperature, till to arrive *{str(temperature_to_reach)}°*\n\n"
                                     f"🧍‍♂️If you have any problem talk with a manager of the infrastracture!")