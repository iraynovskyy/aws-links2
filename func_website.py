import json
import requests


def func_website(message, context):
    response = {}
    try:
        response["callback"] = message["callback"]
    except:
        pass
    response["job_id"] = message["job_id"]
    response["link"] = message["link"]
    response["timestamp"] = message["timestamp"]

    url = message["link"]

    try:
        response["result"] = requests.get(url).elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        print(e)
        response["error"] = "Requesting error"

    return response
