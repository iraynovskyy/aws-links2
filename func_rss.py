import json
import feedparser


def func_rss(message, context):
    response = {}
    try:
        response["callback"] = message["callback"]
    except KeyError:
        pass
    response["job_id"] = message["job_id"]
    response["link"] = message["link"]
    response["timestamp"] = message["timestamp"]

    link = message["link"]
    try:
        dataFeeds = feedparser.parse(link)
        response["result"] = dataFeeds.entries[-5:]

        # test_json = {"testkey": ["valuekey", "value2"], "jjj": "lll"}
        # response["result"] = test_json

        # try:
        #     dataFeeds_5 = dataFeeds.entries[-5:]
        #     Feeds = []
        #     for i in range(len(dataFeeds)):
        #         item = {
        #             'title': dataFeeds_5[i].title,
        #             'type': dataFeeds_5[i].link
        #         }
        #         Feeds.append(item)
        #
        #     response["result"] = {"feeds": Feeds}
        # except:
        #     response["result"] = dataFeeds.entries[-5:]
    except BaseException as e:
        response["error"] = e
    return response
