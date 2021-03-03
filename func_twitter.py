import json


def func_twitter(event, context):
    response = {}
    response["job_id"] = event["job_id"]
    response["link"] = event["link"]
    response["timestamp"] = event["timestamp"]
    link = event["link"]
    response["result"] = "HaD Not sTarTeD iT yEt:)"
    return response
