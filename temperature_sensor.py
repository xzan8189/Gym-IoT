import json
import random

import boto3

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Gym_rooms')

if __name__ == '__main__':
    # Creating Queues
    id_random_gym_room = 1
    random_temperature = 30
    air_conditioner = False

    if random_temperature >= 30:
        air_conditioner = True

    table.update_item(
        Key={'id': id_random_gym_room},
        UpdateExpression= "set temperature = :temperature, air_conditioner = :air_conditioner",
        ExpressionAttributeValues={':temperature': random_temperature,
                                   ':air_conditioner': air_conditioner}
    )

    print(f"id_random_gym_room: {str(id_random_gym_room)}\n"
          f"random_temperature: {str(random_temperature)}\n"
          f"air_conditioner: {str(air_conditioner)}")