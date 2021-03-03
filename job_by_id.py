import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def lambda_handler(event, context):
    data = table.get_item(Key={'job_id': event['job_id']})

    return data["Item"]
