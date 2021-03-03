import requests
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def func_result_processing(message, context):
    if "error" in message:
        state = "error"
        result = message["error"]
    else:
        state = "success"
        result = message["result"]

    table.update_item(
        Key={
            'job_id': message["job_id"]
        },
        UpdateExpression='SET #state = :value, #result = :result, #timestamp = :timestamp',
        ExpressionAttributeValues={
            ':value': state,
            ':result': str(result),
            ':timestamp': str(message["timestamp"])
        },
        ExpressionAttributeNames={
            "#state": "state",
            "#result": "result",
            "#timestamp": "timestamp"
        }
    )
    data = {}
    try:
        if "error" in message:
            data['error'] = message["error"]
        else:
            data['result'] = message["result"]
        requests.post(message["callback"], data=json.dumps(data), headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException:
        return ({"error": "CallbackEr"})
    except KeyError:
        return ({})
