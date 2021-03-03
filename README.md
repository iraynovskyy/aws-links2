### 2nd task AWS
Short explanation: 
* User is able to post list of links as a POST request (example is below)
* These links are checked depending on their type ("Website", "RSS", "Twitter")
  * if "Website" returns time needed to load the page
  * if "RSS" returns last 5 feeds
  * "Twitter" is not implemented yet (but is implemented inside all of the serverless.yml structure)
* If there is "callback" in event (in post request alongside with links) then it will be saved in DynamoDB the same way as the main data about links.
* The saved data about links are: 
  * job_id
  * link (name)
  * linkType
  * result (time, feeds or tweets)
  * timestamp (Seconds since Jan 01 1970)
  * state
  * callback
* Awailable Endpoints:
  * /jobs POST (tested from AWS console)
  * /jobs_all GET all jobs
  * /jobs/{job_id} GET job from DynamoDB by its id
  * /websites GET all jobs which have type of "Website"

##### Needed packages were downloaded from https://pypi.org/ and added locally. Then deployed to AWS by using command $serverless deploy


##### Example of data in POST request (I was testing it from AWS console):
{
  "links": [
    "https://facebook.com",
    "https://investorshub.advfn.com/boards/rss.aspx?board_id=22658",
    "https://tesla.com",
    "https://twitter.com",
    "http://feedparser.org/docs/examples/rss20.xml",
    "https://www.feedotter.com/feed"
  ],
  "callback": "webhook_callback_1"
}
