import requests
import boto3
import datetime
import json

def lambda_handler(event, context):
	key = "8r2OPGW4P30VW-UIpTL_E"
	url = "https://maker.ifttt.com/trigger/email_error/with/key/"+key
	for record in event['Records']:
		payload = record['body']
		payload = json.loads(str(payload))

		# Take data
		device_id = payload['device_id']
		value_time_spent = payload['value_time_spent']
		value_calories_spent = payload['value_calories_spent']

		req = requests.post(url, json={"value1": device_id, "value2": value_time_spent, "value3": value_calories_spent})
