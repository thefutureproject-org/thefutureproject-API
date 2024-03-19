from routers.Database import models
from .make_dict import make_dict
import concurrent.futures
import math
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
import time
import threading

unique_usernames = set()
lock = threading.Lock()


DATABASE_URL = SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def scrape_each_page(page_number: int,  contest_name: str, db):
    try:
        response = requests.get(
            f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination={page_number}&region=global", proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, page: {page_number}")
            scrape_each_page(page_number, contest_name, db)
        else:
            data = response.json()
            questions = data["questions"]
            contestants = data["total_rank"]
            submissions = data["submissions"]
            question_ids = [question['question_id'] for question in questions]

            for contestant, submission in zip(contestants, submissions):
                result = make_dict(contestant, submission, question_ids)
                contestant_info = models.Contest(**result)

                with lock:
                    if contestant_info.username not in unique_usernames:
                        unique_usernames.add(contestant_info.username)
                        db.add(contestant_info)

            print(f"Page {page_number} done")
    except Exception as e:
        print(f"Error occurred: {e}")


def contest_scrape(contest_name: str):
    print(
        f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination=1&region=global")
    response = requests.get(
        f"https://leetcode.com/contest/api/ranking/{contest_name}/?pagination=1&region=global", proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        contest_scrape(contest_name)
    else:
        total_pages = math.ceil(response.json()["user_num"]/25)

        print(total_pages)
        start_time = time.perf_counter()
        db = SessionLocal()

        try:
            # Perform your database operation here
            if db.query(models.Contest).count() > 0:
                db.query(models.Contest).delete()
                db.commit()
        except Exception as e:
            # If an exception occurs, rollback the session
            db.rollback()
            db.query(models.Contest).delete()
            print(f"Error occurred: {e}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(
                scrape_each_page, page, contest_name, db) for page in range(1, total_pages+1)]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Will raise an exception if the thread failed
            except Exception as e:
                print(f"Error in thread: {e}")
                db.rollback()  # Rollback the entire transaction if any thread fails

        db.commit()

        finish_time = time.perf_counter()
        print(
            f"All threads stopped. Finished in {round(finish_time-start_time, 2)} seconds")


contest_scrape("weekly-contest-389")
