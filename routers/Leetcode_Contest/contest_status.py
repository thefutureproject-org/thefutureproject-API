import datetime
import json
from bs4 import BeautifulSoup
import requests

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': 'INGRESSCOOKIE=b818146f6fa0c9fa5d480497ba1f6257|8e0876c7c1464cc0ac96bc2edceabd27; __cf_bm=tDiAcrIZ0x_o1qFHJfE0fq3k1tYF5Ma_vDwn5pITAXQ-1710001249-1.0.1.1-MZCNaeJ._MqFLwXq2iEK1Xh8nypIACK2F2mX51nls_jXnrNb39bTAh3bnH7_qvt3S.0zKiozK8iFfCkshaHkCg; csrftoken=t0ilXJu4pOWzeFwjjagUdXYTKRnlDVDoinStrd491MJDaLLCn3NJu4NgSIur6DMR; _ga_CDRWKZTDEX=GS1.1.1710001254.1.0.1710001254.60.0.0; gr_user_id=4454c391-f9fa-4468-a27c-2de17f146be2; 87b5a3c3f1a55520_gr_session_id=76bc8726-b706-48e9-b807-ac8038cc0c17; 87b5a3c3f1a55520_gr_session_id_sent_vst=76bc8726-b706-48e9-b807-ac8038cc0c17; _ga=GA1.2.600148059.1710001255; _gid=GA1.2.1218620895.1710001255; _gat=1',
    'Dnt': '1',
    'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
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
