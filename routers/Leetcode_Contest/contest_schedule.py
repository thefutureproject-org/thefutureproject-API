# from contest_scrape import contest_scrape
# from contest_status import contest_status
# import sys
from .contest_scrape import contest_scrape
from .contest_status import contest_status
import threading
import time
import datetime
import schedule
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent))


def leetcode_contest_schedule():
    contest = contest_status()
    # print(contest)
    if contest["message"] != "No contest running at the moment.":
        contest_name = contest["message"]["titleSlug"]
        print(f"Scraping {contest_name}...")
        contest_scrape(contest_name)


# Utility function to check if it's the correct biweekly Saturday


def is_second_saturday(date):
    first_target_date = datetime.datetime(2024, 3, 2)
    delta = date - first_target_date
    weeks_since_first_target = delta.days // 7
    return weeks_since_first_target % 2 == 0

# Weekly Contest Scheduler


def schedule_weekly_contest():
    now = datetime.datetime.utcnow()
    end_time = now.replace(hour=4, minute=7, second=0, microsecond=0)
    if now <= end_time:
        leetcode_contest_schedule()
    else:
        return schedule.CancelJob

# Biweekly Contest Scheduler


def schedule_biweekly_contest():
    now = datetime.datetime.utcnow()
    if is_second_saturday(now):
        end_time = now.replace(hour=16, minute=7, second=0, microsecond=0)
        if now <= end_time:
            leetcode_contest_schedule()
        else:
            return schedule.CancelJob

# Setup initial scheduling


def run_scheduler():  # New function to handle the loop
    while True:
        schedule.run_pending()
        time.sleep(1)


def setup_scheduling():
    print("Contest Scheduler is running...")
    # Weekly contest, every Sunday at 2:32 AM UTC
    schedule.every().sunday.at("02:32").do(lambda: schedule.every(
        5).minutes.until("04:07").do(schedule_weekly_contest))

    # Biweekly contest, every second Saturday at 2:32 PM UTC
    schedule.every().saturday.at("14:32").do(lambda: schedule.every(5).minutes.until("16:07").do(
        schedule_biweekly_contest) if is_second_saturday(datetime.datetime.utcnow()) else None)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()


# leetcode_contest_schedule()
