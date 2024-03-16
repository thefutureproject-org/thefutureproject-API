from routers.Database import models
from .make_dict import make_dict
import concurrent.futures
import math
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
import time
from sqlalchemy.exc import IntegrityError
# from sqlalchemy.dialects.postgresql import insert


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

                try:
                    db.add(contestant_info)
                    # db.commit()
                except IntegrityError:
                    # If there is a conflict (duplicate primary key), update the existing row
                    db.rollback()  # Rollback the previous transaction
                    # Merge the new data with the existing row
                    db.merge(contestant_info)
                    # db.commit()  # Commit the merged data to the database

                # insert_stmt = insert(
                #     models.Contest.__table__).values(**result)
                # do_update_stmt = insert_stmt.on_conflict_do_update(
                #     index_elements=['username'], set_=result)
                # db.execute(do_update_stmt)

            print(f"Page {page_number} done")
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
    if db.query(models.Contest).count() > 0:
        db.query(models.Contest).delete()
        db.commit()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(
            scrape_each_page, page, contest_name, db) for page in range(1, total_pages+1)]

    db.commit()

    finish_time = time.perf_counter()
    print(
        f"All threads stopped. Finished in {round(finish_time-start_time, 2)} seconds")


# contest_scrape("biweekly-contest-126")
