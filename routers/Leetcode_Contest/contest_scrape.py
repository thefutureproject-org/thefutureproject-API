# from make_dict import make_dict
# import sys
from routers.Database import models
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from routers.Database.database import get_db
from .make_dict import make_dict
import concurrent.futures
import math
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent))

# import json
import time


# contestants_info = {}


DATABASE_URL = SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def scrape_each_page(page_number: int,  contest_name: str, db):
    try:
        response = requests.get(
            f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination={page_number}&region=global", proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
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
            # db.commit()

    except Exception as e:
        print(f"Error occurred: {e}")


def contest_scrape(contest_name: str):
    print(
        f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination=1&region=global")
    total_pages = math.ceil(requests.get(
        f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination=1&region=global", proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER).json()["user_num"]/25)

    print(total_pages)
    start_time = time.perf_counter()
    db = SessionLocal()
    db.query(models.Contest).delete()
    db.commit()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            scrape_each_page, page, contest_name, db) for page in range(1, total_pages+1)]

    db.commit()

    finish_time = time.perf_counter()
    print(
        f"All threads stopped. Finished in {round(finish_time-start_time, 2)} seconds")

    # with open("contestants_info.json", "w") as file:
    #     json.dump(contestants_info, file, indent=4)


# contest_scrape("biweekly-contest-125")
