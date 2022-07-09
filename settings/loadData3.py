import datetime
from decimal import Decimal
import json
import boto3
from botocore.exceptions import ClientError
from models.User import User

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Gym_rooms')

def load_gym_rooms(gym_rooms):
    for gym_room in gym_rooms['Gym_rooms']:
        #print(f"Adding gym_room: \n{gym_room}")
        table.put_item(Item=gym_room)

if __name__ == '__main__':
    with open("gymRoomData.json") as json_file:
        gym_rooms_list = json.load(json_file, parse_float=Decimal)

    load_gym_rooms(gym_rooms_list)
    #id = input("Write the id of gym room to find: ")
    id = 1

    try:
        response = table.get_item(Key={'id': int(id)})
    except ClientError as e:
        print(e.response['Error']['Message'])

    print("Item: " + str(response['Item']))