# from contest_scrape import contest_scrape
# from contest_status import contest_status
# import sys
from .contest_scrape import contest_scrape
from .contest_status import contest_status
import threading
import time
from datetime import datetime, timedelta
import schedule
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent))


def leetcode_contest_schedule():
    contest = contest_status()
    print("contest scraping running")
    # contest_scrape("weekly-contest-388")
    if contest["message"] != "No contest running at the moment.":
        contest_name = contest["message"]["titleSlug"]
        print(f"Scraping {contest_name}...")
        contest_scrape(contest_name)
    else:
        print("No contest running at the moment.")


# Utility function to check if it's the correct biweekly Saturday


def is_second_saturday(date):
    first_target_date = datetime(2024, 3, 2)
    delta = date - first_target_date
    weeks_since_first_target = delta.days // 7
    return weeks_since_first_target % 2 == 0

# Weekly Contest Scheduler


def schedule_weekly_contest():
    print("Weekly contest checking")
    now = datetime.utcnow()
    end_time = now.replace(hour=4, minute=7, second=0, microsecond=0)
    # leetcode_contest_schedule()

    if now <= end_time:
        leetcode_contest_schedule()
    else:
        return schedule.CancelJob

# Biweekly Contest Scheduler


def schedule_biweekly_contest():
    print("Biweekly contest checking")
    now = datetime.utcnow()
    end_time = now.replace(hour=16, minute=7, second=0, microsecond=0)
    if now <= end_time:
        leetcode_contest_schedule()
    else:
        return schedule.CancelJob

# Setup initial scheduling


def run_scheduler(weekly_scheduler, biweeekly_scheduler):  # New function to handle the loop
    print("Scheduler running...")
    while True:
        weekly_scheduler.run_pending()
        biweeekly_scheduler.run_pending()
        time.sleep(1)


def weekly_every_5_minutes():
    i = 1
    while True:
        schedule_weekly_contest()
        i += 1
        time.sleep(300)
        if (i == 19):
            return


def biweekly_every_5_minutes():
    if is_second_saturday(datetime.utcnow()):
        i = 1
        while True:
            schedule_biweekly_contest()
            i += 1
            time.sleep(300)
            if (i == 19):
                return


def setup_scheduling():
    print("Contest Scheduler is running...")
    # Weekly contest, every Sunday at 2:32 AM UTC
    weekly_scheduler = schedule.Scheduler()
    weekly_scheduler.every().sunday.at(
        "08:02", "Asia/Kolkata").do(weekly_every_5_minutes)

    # Biweekly contest, every second Saturday at 2:32 PM UTC
    biweeekly_scheduler = schedule.Scheduler()
    biweeekly_scheduler.every().saturday.at(
        "20:02", "Asia/Kolkata").do(biweekly_every_5_minutes)

    scheduler_thread = threading.Thread(
        target=run_scheduler, args=(weekly_scheduler, biweeekly_scheduler))
    scheduler_thread.start()


# setup_scheduling()
