import asyncio
import time
import aiohttp
import certifi
import ssl
import datetime
from config import settings


async def fetch_data(session, url, retries=100, delay=0.5):
    for attempt in range(retries):
        try:
            async with session.get(url, proxy=settings.PROXY_URL) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(
                        f'API request failed with status code {response.status}, retrying... (Attempt {attempt + 1} of {retries})')
        except Exception as e:
            print(
                f'Error during request: {str(e)}, retrying... (Attempt {attempt + 1} of {retries})')
        await asyncio.sleep(delay)
    return f'API request failed after {retries} attempts'


async def get_data_for_pages(weekly_contest):
    try:
        base_api_url = f'https://leetcode.com/contest/api/ranking/{weekly_contest}/?pagination={{}}&region=global'

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector, headers=settings.LEETCODE_HEADER, trust_env=True) as session:
            tasks = []
            for page in range(1, 1000):
                api_url = base_api_url.format(page)
                tasks.append(fetch_data(session, api_url))

            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()

            time_taken = end_time-start_time

            return results

    except Exception as e:
        return [f'Error making API request: {str(e)}']


def submission_time_graph_data_solve(data, total_time=90):
    if data:
        submission_map = {}
        minimum_hour = float('inf')
        for entry in data:
            submissions = entry.get("submissions", [])
            for submission in submissions:
                for question_id, submission_data in submission.items():
                    submission_time = submission_data.get("date", 0)
                    submission_datetime = datetime.datetime.fromtimestamp(
                        submission_time)
                    minimum_hour = min(minimum_hour, submission_datetime.hour)

        for entry in data:
            submissions = entry.get("submissions", [])
            for submission in submissions:
                for question_id, submission_data in submission.items():
                    question_id = str(question_id)
                    submission_time = submission_data.get("date", 0)
                    submission_datetime = datetime.datetime.fromtimestamp(
                        submission_time)
                    minute_key = (submission_datetime.hour -
                                  minimum_hour) * 60 + submission_datetime.minute

                    if question_id not in submission_map:
                        submission_map[question_id] = {}

                    if minute_key not in submission_map[question_id]:
                        submission_map[question_id][minute_key] = 0

                    submission_map[question_id][minute_key] += 1

        for question_id, time_data in submission_map.items():
            sorted_times = sorted(time_data.items())
            prefix_sum = 0

            for minute_key, count in sorted_times:
                prefix_sum += count
                time_data[minute_key] = prefix_sum

            existing_minutes = list(time_data.keys())
            for minute in range(1, total_time):
                if minute not in existing_minutes:
                    prev_minute = max(
                        filter(lambda x: x < minute, existing_minutes), default=None)
                    next_minute = min(
                        filter(lambda x: x > minute, existing_minutes), default=None)

                    if prev_minute is not None and next_minute is not None:
                        time_data[minute] = (
                            time_data[prev_minute] + time_data[next_minute]) // 2
                    elif prev_minute is not None:
                        time_data[minute] = time_data[prev_minute]
                    elif next_minute is not None:
                        time_data[minute] = time_data[next_minute]

        return submission_map
    else:
        print("No JSON data found in the response.")


def segregate_users_by_country(all_submissions):
    try:
        segregated_data = {}
        segregated_data[""] = []

        for item in all_submissions:
            total_rank = item.get("total_rank", [])

            for user_data in total_rank:
                username = user_data.get("username")
                country_name = user_data.get("country_name")
                rank = user_data.get("rank")

                if country_name is not None and country_name != "":
                    if country_name not in segregated_data:
                        segregated_data[country_name] = []

                    segregated_data[country_name].append({
                        "username": username,
                        "realrank": rank,
                        "country_name": country_name,
                        "country_rank": len(segregated_data[country_name]) + 1,
                    })
                else:
                    segregated_data[""].append({
                        "username": username,
                        "realrank": rank,
                        "country_name": "",
                        "country_rank": len(segregated_data[""]) + 1,
                    })

        for country_name, users in segregated_data.items():
            segregated_data[country_name] = sorted(
                users, key=lambda x: x["realrank"])

        return segregated_data

    except Exception as e:
        print({'error': str(e)})


def count_fail_counts(all_submissions):
    fail_count_stats = {}

    for submissions in all_submissions:
        # print(type(submissions))
        # print(submissions)
        for submission in submissions.get("submissions", []):
            for question_id, submission_data in submission.items():
                fail_count = submission_data.get("fail_count", 0)

                if question_id not in fail_count_stats:
                    fail_count_stats[question_id] = {
                        "0": 0, "1": 0, "2": 0, "3": 0, "4+": 0}

                if fail_count == 0:
                    fail_count_stats[question_id]["0"] += 1
                elif fail_count == 1:
                    fail_count_stats[question_id]["1"] += 1
                elif fail_count == 2:
                    fail_count_stats[question_id]["2"] += 1
                elif fail_count == 3:
                    fail_count_stats[question_id]["3"] += 1
                else:
                    fail_count_stats[question_id]["4+"] += 1

    return fail_count_stats


def get_questions(all_submissions):
    fail_count_stats = count_fail_counts(all_submissions)

    questions = all_submissions[0].get("questions", [])
    for question in questions:
        question_id = str(question.get("question_id"))
        if question_id in fail_count_stats:
            question["fail_count"] = fail_count_stats[question_id]
        else:
            question["fail_count"] = {"0": 0, "1": 0, "2": 0, "3": 0, "4+": 0}

    for question in questions:
        question["codeforces_rating"] = 0
        question["author"] = "Leetcode Company"
        question["inspired_from"] = "Uber OA"

    return questions


async def get_all_submissions(weekly_contest: str = 'weekly-contest-403', username: str = 'NayakPenguin'):
    all_submissions = await get_data_for_pages(weekly_contest)
    # print(all_submissions)
    questions = get_questions(all_submissions)

    computed_data = {
        'submission_map': submission_time_graph_data_solve(all_submissions),
        'rank_by_country': segregate_users_by_country(all_submissions),
        'questions': questions
    }

    return computed_data
