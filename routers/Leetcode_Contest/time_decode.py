import datetime


def calculate_submission_time(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    contest_1_start = dt_object.replace(
        hour=8, minute=0, second=0, microsecond=0)
    contest_2_start = dt_object.replace(
        hour=20, minute=0, second=0, microsecond=0)
    time_diff_1 = dt_object - contest_1_start
    time_diff_2 = dt_object - contest_2_start
    if abs(time_diff_1.total_seconds()) < abs(time_diff_2.total_seconds()):
        nearest_contest_start = contest_1_start
    else:
        nearest_contest_start = contest_2_start
    submission_time = dt_object - nearest_contest_start
    return str(submission_time)
