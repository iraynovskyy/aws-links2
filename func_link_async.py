import json
import os
import uuid
import boto3
from urllib.parse import urlparse
import feedparser
import asyncio
from aiohttp import ClientSession, client_exceptions

CLIENT = boto3.client('stepfunctions')
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


async def fetch(session, link):
    job_id = str(uuid.uuid1())  # 90a0fce-sfhj45-fdsfsjh4-f23f

    input = {}
    input["job_id"] = job_id
    input["link"] = link

    async with session.get(link):
        CLIENT.start_execution(
            stateMachineArn=os.environ["STATE_MACHINE"],
            name=job_id,
            input=json.dumps(
                {'job_id': job_id, 'link': link, })
        )
    item = {
        'job_id': job_id,
        'link': link
    }
    table.put_item(Item=item)
    return {link: job_id}


async def main(links):
    async with ClientSession() as session:
        tasks = []
        for link in links:
            tasks.append(fetch(session, link))
        return await asyncio.gather(*tasks)


def lambda_handler(event, context):
    # input = {"links": ["https://google.com", "https://cat.com"]}
    links = ["https://google.com", "https://cat.com"]

    body = {}
    for k in asyncio.run(main(links)):
        body.update(k)
    return {
        'statusCode': 200,
        'body': body,
    }

# asyncio.run(main())
