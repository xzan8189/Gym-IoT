import boto3

dynamobdb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamobdb.create_table( # Creating table 'Users'
    TableName='Users',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH' #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

dynamobdb.create_table( # Creating table 'Training_cards'
    TableName='Training_cards',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH' #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

dynamobdb.create_table( # Creating table 'Gym_rooms'
    TableName='Gym_rooms',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH' #Partition key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    },
    StreamSpecification={
        'StreamEnabled': True,
        'StreamViewType': 'NEW_IMAGE'
    }
)