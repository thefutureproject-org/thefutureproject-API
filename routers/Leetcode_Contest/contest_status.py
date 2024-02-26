import datetime
import json
from bs4 import BeautifulSoup
import requests


def decode_timestamp(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=datetime.timezone.utc)


def is_contest_running(start_timestamp):
    decoded_start = decode_timestamp(start_timestamp)
    current_time = datetime.datetime.now(datetime.timezone.utc)

    if current_time >= decoded_start:
        return "Contest Running"
    else:
        return "Not Running"


def contest_status():
    response = requests.get("https://leetcode.com/contest/").text
    soup = BeautifulSoup(response, 'html.parser')
    json_data = soup.find('script', id='__NEXT_DATA__').string
    json_data = json.loads(json_data)
    response = json_data['props']['pageProps']['dehydratedState']['queries'][4]['state']['data']['topTwoContests']
    # print(response)
    for contest in response:
        contest_status = is_contest_running(contest["startTime"])
        if contest_status == "Contest Running":
            return {"message": {"title": contest["title"], "titleSlug": contest["titleSlug"], "status": contest_status}}

    return {"message": "No contest running at the moment."}
