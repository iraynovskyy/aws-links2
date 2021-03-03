import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def lambda_jobs_get_all(event, context):
    resp = table.scan()
    records = []

    for item in resp['Items']:
        records.append(item)

    response = {
        "statusCode": 200,
        "body": records
    }
    # return {"jobs": records}
    return response
