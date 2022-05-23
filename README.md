# IOT Gym using Serverless Computing

## Overview

Gym IoT is a gym that measures the calories consumed by the client, providing him a constant report on the progress of his workout.
Inside the gyms there are machines that record informations about the calories consumed and the duration of the workout, but unfortunately these informations are ephemerals, they are not stored in any way (in a database) and for this reason there is no possibility to double-check these informations to understand how to improve your workout!

IoT Gym was created for this purpose, based on the informations collected from the training sessions, graphs are built, which can be viewed from the web-site, so as to keep track of the following informations:

* **Calories consumed** and **Time of use** on each machine in the gym
* **Total calories consumed each month** (you can compare the calories consumed in the current year with those in the previous year)
* **Calories consumed during the day**

The IoT sensors, positioned inside the machines, can  **measure incorrectly** the calories consumed and/or the time of use on the machine. If this occurs, a message is sent on the Error queue which triggers a Serverless Function which sends an email containing the <code>device ID</code>, which generated the error, the <code>value_time_spent</code> (usage time) and the <code>value_calories_spent</code> (calories consumed)


<div align="center">
<img src="./images/IFTTT.png" alt="loading..." width="80%" >
</div>

## Architecture

<div align="center">
<img src="./images/Architettura (image).png" alt="loading..." width="100%" >
</div>

* The Cloud environment is simulated using [LocalStack](https://localstack.cloud/) to replicate the [AWS services](https://aws.amazon.com/)
* The IoT devices are simulated with a Python function using [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) to send messages on the queues.
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) is the service used to built the database.
* The DynamoDB GUI is available using dynamodb-admin.
* The queues are implemented using [Amazon Simple Queue Service (SQS)](https://aws.amazon.com/sqs/)
* The functions are Serveless functions deployed on [AWS Lambda](https://aws.amazon.com/lambda/)
	* The time-triggered function is implemented using [Amazon EventBridge](https://aws.amazon.com/eventbridge/)
* The error email is sent using [IFTT](https://ifttt.com/)

## Installation and usage

### Prerequisites
1. [Docker](https://docs.docker.com/get-docker/)
2. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
4. [Flask](https://flask.palletsprojects.com/en/2.1.x/)

### Setting up the environment

**0. Clone the repository**

```bash
git clone https://github.com/xzan8189/Gym-IoT.git
```

**1. Launch [LocalStack](https://localstack.cloud/)**

```bash
docker run --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack
```

**2. Create a SQS queue for each machine**

```bash
aws sqs create-queue --queue-name Cyclette --endpoint-url=http://localhost:4566
aws sqs create-queue --queue-name Tapis_roulant --endpoint-url=http://localhost:4566
aws sqs create-queue --queue-name Elliptical_bike --endpoint-url=http://localhost:4566
aws sqs create-queue --queue-name Spin_bike --endpoint-url=http://localhost:4566
aws sqs create-queue --queue-name Errors --endpoint-url=http://localhost:4566
```

* Check that the queues are been correctly created

```bash
aws sqs list-queues --endpoint-url=http://localhost:4566
```

**3. Create the DynamoDB table and populate it**

1. Use the python code to create the DynamoDB table
```bash
python3 settings/createTable.py
```

2. Check that the table is been correctly created
```bash
aws dynamodb list-tables --endpoint-url=http://localhost:4566
```

3. Populate the tables with some data, but before set `PYTHONPATH` environment variable in root project directory
```bash
export PYTHONPATH=.
```

and finally:

```bash
python3 settings/loadData.py
```

4. Check that the table are been correctly populated using the AWS CLI (Press q to exit)
```bash
aws dynamodb scan --table-name Users --endpoint-url=http://localhost:4566
```

or using the (dynamodb-admin) GUI with the command
```bash
DYNAMO_ENDPOINT=http://0.0.0.0:4566 dynamodb-admin
```

and then going to http://localhost:8001

**4. Create the time-triggered Lambda function to elaborate the data**

1. Create the role
```bash
aws iam create-role --role-name lambdarole --assume-role-policy-document file://settings/role_policy.json --query 'Role.Arn' --endpoint-url=http://localhost:4566
```

2. Attach the policy 
```bash
aws iam put-role-policy --role-name lambdarole --policy-name lambdapolicy --policy-document file://settings/policy.json --endpoint-url=http://localhost:4566
```

3. Create the zip file
```bash
zip updateUserFunc.zip settings/updateUserFunc.py
```

4. Create the function and save the Arn (it should be something like <code>arn:aws:lambda:us-east-2:000000000000:function:updateUserFunc</code>


```bash
aws lambda create-function --function-name updateUserFunc --zip-file fileb://updateUserFunc.zip --handler settings/updateUserFunc.lambda_handler --runtime python3.8 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566
```

> if you want delete the lambda function, digit this:
```bash
aws lambda delete-function --function-name updateUserFunc --endpoint-url=http://localhost:4566
```

5. Test the function:

	* create an user in the **sign-up page** with *username="prova"*

	* simulate the messages sent by some IoT devices
	```bash
	python3 IotDevices.py
	```

	* manually invoke the function (it may take some times)
	```bash
	aws lambda invoke --function-name updateUserFunc out --endpoint-url=http://localhost:4566
	```

	* check within the table that the item with *username="prova"* is changed

6. From here you could jump directly to the [Use it](#use-it) step and run the website to check the changes of the user, logging with his credentials.

**5. Set up a CloudWatch rule to trigger the Lambda function every 1 minute**

1. Creare the rule and save the Arn (it should be something like <code>arn:aws:events:us-east-2:000000000000:rule/updateUser</code>)
```bash
aws events put-rule --name updateUser --schedule-expression 'rate(1 minutes)' --endpoint-url=http://localhost:4566
```

2. Check that the rule has been correctly created with the frequency wanted
```bash
aws events list-rules --endpoint-url=http://localhost:4566
```

3. Add permissions to the rule created
```bash
aws lambda add-permission --function-name updateUserFunc --statement-id updateUser --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn arn:aws:events:us-east-2:000000000000:rule/updateUserFunc --endpoint-url=http://localhost:4566
```

4. Add the lambda function to the rule using the JSON file containing the Lambda function Arn
```sh
aws events put-targets --rule updateUser --targets file://settings/targets.json --endpoint-url=http://localhost:4566
```

Now every 1 minute the function *updateUserFunc* will be triggered.

**6. Set up the Lambda function triggered by SQS messages that notifies errors in IoT devices via email**

1) Create the IFTT Applet
	1. Go to https://ifttt.com/ and sign-up or log-in if you already have an account.
	2. On the main page, click *Create* to create a new applet.
	3. Click "*If This*", type *"webhooks"* in the search bar, and choose the *Webhooks* service.
	4. Select "*Receive a web request*" and write *"email_error"* in the "*Event Name*" field. Save the event name since it is required to trigger the event. Click *Create trigger*.
	5. In the applet page click *Then That*, type *"email"* in the search bar, and select *Email*.
	6. Click *Send me an email* and fill the fields as follow:
		
		* *Subject*: <code>[GymIoT] Attention a device encountered an error!</code>
		* *Body*: <code><b>Device_id</b>: {{Value1}}<br>
				  <b>When</b>: {{OccurredAt}}<br>
				  <b>Extra Data</b>:<br>
				  value_time_spent: {{Value2}},<br>
				  value_calories_spent: {{Value3}}</code>
			
	7. Click *Create action*, *Continue*, and *Finish*.

2) Modify the variable `IFTTT_EVENT_EMAIL_ERROR` within the `config.py` function with your IFTT applet key. The key can be find clicking on the icon of the webhook and clicking on *Documentation*.

3) Zip the Python file and create the Lambda function
```bash
zip emailError.zip settings/emailError.py settings/config.py
```

```bash
aws lambda create-function --function-name emailError --zip-file fileb://emailError.zip --handler settings/emailError.lambda_handler --runtime python3.8 --role arn:aws:iam::000000000000:role/lambdarole --endpoint-url=http://localhost:4566
```

> if you want delete the lambda function, digit this:
```sh
aws lambda delete-function --function-name emailError --endpoint-url=http://localhost:4566
```

4) Create the event source mapping between the funcion and the queue
```sh
aws lambda create-event-source-mapping --function-name emailError --batch-size 5 --maximum-batching-window-in-seconds 60 --event-source-arn arn:aws:sqs:us-east-2:000000000000:Errors --endpoint-url=http://localhost:4566
```

5) Test the mapping sending a message on the error queue and check that an email is sent
```sh
aws sqs send-message --queue-url http://localhost:4566/000000000000/Errors --message-body '{"device_id": "Cyclette","value_time_spent": "ERROR","value_calories_spent": "ERROR"}' --endpoint-url=http://localhost:4566
```

### Use it
1. Simulate the IoT devices
```bash
python3 IoTdevices.py
```

2. Wait that the Lambda function *updateUserFunc* compute the data (wait 1 minute) or invoke it manually

3. Modify the variable `SECRET_KEY` within the `config.py` with a random string.

4. Run flask with the command:
```bash
export FLASK_APP=./main.py; flask run
```

4. Go to the Website and see the new computed informations

## Future developments

* **Track the change of the weight**: Ability to track the change in your weight over the weeks/months
* **Improving the user-experience**: Providing to the customer a history of all the graphs, so that he can constantly compare with himself (many times this is the best way to improve)
* **Training Card**: Recommending a training schedule based on the customer’s performance, which contains all the machines and exercises to execute.