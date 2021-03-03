import json
import os
from datetime import datetime
import uuid
import boto3
from urllib.parse import urlparse
import feedparser

'''
INPUT = {
  "links": [
    "https://facebook.com",
    "https://investorshub.advfn.com/boards/rss.aspx?board_id=22658",
    "https://tesla.com",
    "https://twitter.com",
    "http://feedparser.org/docs/examples/rss20.xml",
    "https://www.feedotter.com/feed"
  ]
}
'''

CLIENT = boto3.client('stepfunctions')
CLIENT_db = boto3.client('dynamodb')
REGION = os.environ.get('us-east-2')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])


def link_type(url):
    link = urlparse(url)

    if link.hostname in ("twitter.com", "twittter.com", "twttr.com", "www.twitter.fr", "www.twitter.jp"):
        return "Twitter"
    elif len(feedparser.parse(url).entries) != 0:
        return "RSS"
    else:
        return "Website"


def lambda_handler(event, context):
    try:
        links = list(event["links"])
    except KeyError:
        return {
            'Error': "Links are not provided 007"
        }

    if "callback" in event:
        callback = event["callback"]

    response = []
    for link in links:
        job_id = str(uuid.uuid1())  # 90a0fce-sfhj45-fdsfsjh4-f23f

        input = {}

        input["job_id"] = job_id
        input["link"] = link
        input["timestamp"] = str(datetime.now().timestamp())
        input["linkType"] = link_type(link)
        try:
            input["callback"] = callback
        except:
            pass

        CLIENT.start_execution(
            stateMachineArn=os.environ["STATE_MACHINE"],
            name=job_id,
            input=json.dumps(input)
        )

        item = {
            'job_id': job_id,
            'timestamp': input["timestamp"],
            'link': link,
            'linkType': input["linkType"],
            'state': 'Processing'
        }
        try:
            item['callback'] = callback
            print('callback was included in this event.')
        except UnboundLocalError:
            pass

        table.put_item(Item=item)
        response.append(job_id)

    return {"jobs_id": response}
