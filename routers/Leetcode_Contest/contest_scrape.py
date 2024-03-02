import requests
# import json
import math
import concurrent.futures
# import time
from .make_dict import make_dict
from ..Database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from ..Database import models

# contestants_info = {}


def scrape_each_page(page_number: int,  contest_name: str, db):
    try:
        response = requests.get(
            f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination={page_number}&region=global", proxies={
                "http": "http://nvkgvyfp-rotate:kccxhfu1bt2o@p.webshare.io:80/",
                "https": "http://nvkgvyfp-rotate:kccxhfu1bt2o@p.webshare.io:80/"
            })
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data = response.json()
        questions = data["questions"]
        contestants = data["total_rank"]
        submissions = data["submissions"]
        question_ids = [question['question_id'] for question in questions]
        for contestant, submission in zip(contestants, submissions):
            result = make_dict(contestant, submission, question_ids)
            # contestants_info[contestant["username"]] = result
            contestant_info = models.Contest(**result)
            db.add(contestant_info)

    except Exception as e:
        print(f"Error occurred: {e}")


def contest_scrape(contest_name: str, db: Session = Depends(get_db)):

    total_pages = math.ceil(requests.get(
        f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination=1&region=global").json()["user_num"]/25)

    # start_time = time.perf_counter()
    sql_query = f'TRUNCATE TABLE {contest_name};'
    db.execute(sql_query)
    db.commit()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            scrape_each_page, page, contest_name, db) for page in range(1, total_pages+1)]

    db.commit()

    # finish_time = time.perf_counter()
    # print(
    #     f"All threads stopped. Finished in {round(finish_time-start_time, 2)} seconds")

    # with open("contestants_info.json", "w") as file:
    #     json.dump(contestants_info, file, indent=4)
