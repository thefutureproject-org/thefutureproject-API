import datetime
import json
from bs4 import BeautifulSoup
import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Content-Type": "application/json",
    "Cookie": "gr_user_id=51d0183d-ab1c-4871-afd5-228c18e29f94; __stripe_mid=35818f02-963e-4c37-a4c8-15e32ca32953d289ee; _gid=GA1.2.1526224102.1710048293; cf_clearance=zbG.XWfVkgtecc9JH9nEL5SOQBg3nys_mKGVmJ52910-1710048301-1.0.1.1-O7F8ubxCXJzMiAOYuY76WBATmTXzwWVDddNCxE0zSAe3wTiOdKl5PfkPJNpgYt5wgSFKzQmdHttnqvaSNlP9lQ; csrftoken=btesnVn0Gq2RJcoWGt8I3PKoRXda93zTRFqZDTNhu7UkSvo622KLJ4ZULLAWh3mt; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiODQyOTg2NSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImI2Zjc2Njc2MzQ4YjhiNzI4ZjExMzk4NGE2MjA3MGZmNTk3ZjcxMWNkNDBjYTdlOWNiMGQ0MmFlMDNmYjUzZTIiLCJpZCI6ODQyOTg2NSwiZW1haWwiOiJmcmVlcGFpZHVkZW15Y291cnNlc0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImZyZWVwYWlkdWRlbXljb3Vyc2VzIiwidXNlcl9zbHVnIjoiZnJlZXBhaWR1ZGVteWNvdXJzZXMiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY3MzA3MzE3OC5wbmciLCJyZWZyZXNoZWRfYXQiOjE3MTAwNDgzMTIsImlwIjoiMTAzLjEzNS4yMjkuMjQ5IiwiaWRlbnRpdHkiOiJkZDc4ODc4YmViYzBlNmFmZmY4MGJlOTY1MTY1MTFkNyIsInNlc3Npb25faWQiOjU3Mjg3ODY5LCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDB9.g_xuLX6DbOVnWpvR7kYPgkM8kToq0Skt8Ry5t4hWjjM; 87b5a3c3f1a55520_gr_last_sent_cs1=freepaidudemycourses; __gads=ID=2cb691a040adde1d:T=1710048315:RT=1710048315:S=ALNI_MZww2ipnXDoC51WFLfY32i7UQPNZg; __gpi=UID=00000d2f93c85b55:T=1710048315:RT=1710048315:S=ALNI_MYtrUhztV5CtgdfRq5C62O_K7tnBw; __eoi=ID=53099a8ad5ba4afb:T=1710048315:RT=1710048315:S=AA-AfjYwq21NJXs3fS4YMC1dxLy2; FCNEC=%5B%5B%22AKsRol86cwokujtQEa70L6Ng6i6sd73M4o5w-fKZb9P9tyDVecADQIyGBmQZplTZgOl4gvp8jKKWL8nC3t_cC9jaaG3kZmkEozA08WWs3JlMqVnVictxeSINt-xcHssi3DSh-puTjMhGig25l_JU1msrsF4E--q8Vw%3D%3D%22%5D%5D; __cf_bm=8Yeh34SmfgpWMV5R9EuagVhJAijJsWGvYlWD8_1sI6w-1710069277-1.0.1.1-u_UvHYx5fTcj8z7hEFWw8UbP6GG8YpQJ.greJr7L4B5b7CsVApDRFgEqz7N9bS3_7FsxXbcPbIu78jX0Y9ghzA; 87b5a3c3f1a55520_gr_session_id=7298b5e9-1702-4be3-8877-98265e4322f6; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=7298b5e9-1702-4be3-8877-98265e4322f6; 87b5a3c3f1a55520_gr_session_id_sent_vst=7298b5e9-1702-4be3-8877-98265e4322f6; INGRESSCOOKIE=1ef86ac522d87d64b05da611751763dd|8e0876c7c1464cc0ac96bc2edceabd27; _ga=GA1.1.1173200283.1696434674; _ga_CDRWKZTDEX=GS1.1.1710069278.11.1.1710069294.44.0.0; _dd_s=rum=0&expire=1710070646340; 87b5a3c3f1a55520_gr_cs1=freepaidudemycourses; _gat=1",
    "Referer": "https://leetcode.com/contest/weekly-contest-388/ranking/4/",
    "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "X-Newrelic-Id": "UAQDVFVRGwIBVFFQDgIHXlM=",
    "X-Requested-With": "XMLHttpRequest"
}


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
    response = requests.get("https://leetcode.com/contest/", proxies={
        "http": "http://nvkgvyfp-rotate:kccxhfu1bt2o@p.webshare.io:80/",
                "https": "http://nvkgvyfp-rotate:kccxhfu1bt2o@p.webshare.io:80/"}, headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')
    # print(soup)
    json_data = soup.find('script', id='__NEXT_DATA__').string
    json_data = json.loads(json_data)
    response = json_data['props']['pageProps']['dehydratedState']['queries'][4]['state']['data']['topTwoContests']
    # print(response)
    for contest in response:
        contest_status = is_contest_running(contest["startTime"])
        if contest_status == "Contest Running":
            return {"message": {"title": contest["title"], "titleSlug": contest["titleSlug"], "status": contest_status}}

    return {"message": "No contest running at the moment."}
