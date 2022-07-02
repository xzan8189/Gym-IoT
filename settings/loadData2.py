import datetime
from decimal import Decimal
import json
import boto3
from botocore.exceptions import ClientError
from models.User import User

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table = dynamodb.Table('Training_cards')

def load_training_cards(training_cards):
    for training_card in training_cards['Training_cards']:
        #print(f"Adding training_card: \n{training_card}")
        table.put_item(Item=training_card)

if __name__ == '__main__':
    with open("trainingCardData.json") as json_file:
        training_cards_list = json.load(json_file, parse_float=Decimal)

    load_training_cards(training_cards_list)
    id = input("Write the id of tranining card to find: ")

    try:
        response = table.get_item(Key={'id': str(id)})
    except ClientError as e:
        print(e.response['Error']['Message'])


    print(str(response['Item']))
    for item in response['Item']['content']['calories_or_repetitions']:
        if type(item) is Decimal:
            print(str(item) + " ")
        else:
            print(item + " ")