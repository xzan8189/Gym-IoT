import boto3
#sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

client = boto3.client('sqs', endpoint_url='http://localhost:4566')

response = client.list_queues(QueueNamePrefix="")

print(response["QueueUrls"])

client.delete_queue(
    QueueUrl='http://localhost:4566/000000000000/Salerno'
)