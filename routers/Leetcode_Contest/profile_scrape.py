import requests
from config import settings
import concurrent.futures
from fastapi import HTTPException, status

url = "https://leetcode.com/graphql/"


def get_profile_info(username: str, data: dict):
    payload = {"query": "\n    query userPublicProfile($username: String!) {\n  matchedUser(username: $username) {\n    contestBadge {\n      name\n      expired\n      hoverText\n      icon\n    }\n    username\n    githubUrl\n    twitterUrl\n    linkedinUrl\n    profile {\n      ranking\n      userAvatar\n      realName\n      aboutMe\n      school\n      websites\n      countryName\n      company\n      jobTitle\n      skillTags\n      postViewCount\n      postViewCountDiff\n      reputation\n      reputationDiff\n      solutionCount\n      solutionCountDiff\n      categoryDiscussCount\n      categoryDiscussCountDiff\n    }\n  }\n}\n    ", "variables": {"username": username}, "operationName": "userPublicProfile"}
    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        get_profile_info(username)
    else:
        if "errors" not in response.json():
            response = response.json()
            data["username"] = response["data"]["matchedUser"]["username"]
            if response["data"]["matchedUser"]["contestBadge"] is not None:
                data["contestBadge"] = response["data"]["matchedUser"]["contestBadge"]["name"]
            else:
                data["contestBadge"] = None
            data["githubUrl"] = response["data"]["matchedUser"]["githubUrl"]
            data["twitterUrl"] = response["data"]["matchedUser"]["twitterUrl"]
            data["linkedinUrl"] = response["data"]["matchedUser"]["linkedinUrl"]
            if response["data"]["matchedUser"]["profile"] is not None:
                data["ranking"] = response["data"]["matchedUser"]["profile"]["ranking"]
                data["realName"] = response["data"]["matchedUser"]["profile"]["realName"]
                data["aboutMe"] = response["data"]["matchedUser"]["profile"]["aboutMe"]
                data["school"] = response["data"]["matchedUser"]["profile"]["school"]
                data["websites"] = response["data"]["matchedUser"]["profile"]["websites"]
                data["countryName"] = response["data"]["matchedUser"]["profile"]["countryName"]
                data["skillTags"] = response["data"]["matchedUser"]["profile"]["skillTags"]
                data["postViewCount"] = response["data"]["matchedUser"]["profile"]["postViewCount"]
                data["postViewCountDiff"] = response["data"]["matchedUser"]["profile"]["postViewCountDiff"]
                data["reputation"] = response["data"]["matchedUser"]["profile"]["reputation"]
                data["reputationDiff"] = response["data"]["matchedUser"]["profile"]["reputationDiff"]
                data["solutionCount"] = response["data"]["matchedUser"]["profile"]["solutionCount"]
                data["solutionCountDiff"] = response["data"]["matchedUser"]["profile"]["solutionCountDiff"]
                data["categoryDiscussCount"] = response["data"]["matchedUser"]["profile"]["categoryDiscussCount"]
                data["categoryDiscussCountDiff"] = response["data"]["matchedUser"]["profile"]["categoryDiscussCountDiff"]


def get_problem_solved_language_count(username: str, data: dict):
    payload = {"query": "\n    query languageStats($username: String!) {\n  matchedUser(username: $username) {\n    languageProblemCount {\n      languageName\n      problemsSolved\n    }\n  }\n}\n    ", "variables": {
        "username": username}, "operationName": "languageStats"}

    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        get_problem_solved_language_count(username)
    else:
        if "errors" not in response.json():
            response = response.json()
            data["languageProblemCount"] = response["data"]["matchedUser"]["languageProblemCount"]


def get_tag_problem_count(username: str, data: dict):
    payload = {"query": "\n    query skillStats($username: String!) {\n  matchedUser(username: $username) {\n    tagProblemCounts {\n      advanced {\n        tagName\n        tagSlug\n        problemsSolved\n      }\n      intermediate {\n        tagName\n        tagSlug\n        problemsSolved\n      }\n      fundamental {\n        tagName\n        tagSlug\n        problemsSolved\n      }\n    }\n  }\n}\n    ", "variables": {
        "username": username}, "operationName": "skillStats"}
    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        get_tag_problem_count(username)
    else:
        if "errors" not in response.json():
            response = response.json()
            data["tagProblemCounts"] = response["data"]["matchedUser"]["tagProblemCounts"]


def get_user_contest_ranking(username: str, data: dict):
    payload = {"query": "\n    query userContestRankingInfo($username: String!) {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    globalRanking\n    totalParticipants\n    topPercentage\n    badge {\n      name\n    }\n  }\n  userContestRankingHistory(username: $username) {\n    attended\n    trendDirection\n    problemsSolved\n    totalProblems\n    finishTimeInSeconds\n    rating\n    ranking\n    contest {\n      title\n      startTime\n    }\n  }\n}\n    ", "variables": {
        "username": username}, "operationName": "userContestRankingInfo"}

    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        get_user_contest_ranking(username)
    else:
        if "errors" not in response.json():
            response = response.json()
            data["userContestRanking"] = response["data"]["userContestRanking"]
            del data["userContestRanking"]["totalParticipants"]


def get_total_problems_solved(username: str, data: dict):
    payload = {"query": "\n    query userProblemsSolved($username: String!) {\n  allQuestionsCount {\n    difficulty\n    count\n  }\n  matchedUser(username: $username) {\n    problemsSolvedBeatsStats {\n      difficulty\n      percentage\n    }\n    submitStatsGlobal {\n      acSubmissionNum {\n        difficulty\n        count\n      }\n    }\n  }\n}\n    ", "variables": {
        "username": username}, "operationName": "userProblemsSolved"}

    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        get_total_problems_solved(username)
    else:
        if "errors" not in response.json():
            response = response.json()
            data["total_problems_solved"] = response["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]


def get_submmission_calender(username: str, data: dict):
    payload = {"query": "\n    query userProfileCalendar($username: String!, $year: Int) {\n  matchedUser(username: $username) {\n    userCalendar(year: $year) {\n      activeYears\n      streak\n      totalActiveDays\n      dccBadges {\n        timestamp\n        badge {\n          name\n          icon\n        }\n      }\n      submissionCalendar\n    }\n  }\n}\n    ", "variables": {
        "username": username}, "operationName": "userProfileCalendar"}

    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        get_submmission_calender(username)
    else:
        if "errors" not in response.json():
            response = response.json()
            data["submissionCalendar"] = response["data"]["matchedUser"]["userCalendar"]["submissionCalendar"]


def user_info(username: str):
    data = {
        "username": None,
        "contestBadge": None,
        "githubUrl": None,
        "twitterUrl": None,
        "linkedinUrl": None,
        "ranking": None,
        "realName": None,
        "aboutMe": None,
        "school": None,
        "websites": None,
        "countryName": None,
        "skillTags": None,
        "postViewCount": None,
        "postViewCountDiff": None,
        "reputation": None,
        "reputationDiff": None,
        "solutionCount": None,
        "solutionCountDiff": None,
        "categoryDiscussCount": None,
        "categoryDiscussCountDiff": None,
        "languageProblemCount": None,
        "tagProblemCounts": None,
        "userContestRanking": None,
        "total_problems_solved": None,
        "submissionCalendar": None
    }
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_profile_info = executor.submit(get_profile_info, username, data)
        future_problem_solved_language_count = executor.submit(
            get_problem_solved_language_count, username, data)
        future_tag_problem_count = executor.submit(
            get_tag_problem_count, username, data)
        future_user_contest_ranking = executor.submit(
            get_user_contest_ranking, username, data)
        future_total_problems_solved = executor.submit(
            get_total_problems_solved, username, data)
        future_submmission_calender = executor.submit(
            get_submmission_calender, username, data)

    concurrent.futures.wait([
        future_profile_info,
        future_problem_solved_language_count,
        future_tag_problem_count,
        future_user_contest_ranking,
        future_total_problems_solved,
        future_submmission_calender
    ])

    if (data["username"] is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return data


# {'errors': [{'message': 'That user does not exist.', 'locations': [{'line': 3, 'column': 3}],
#              'path': ['matchedUser'], 'extensions': {'handled': True}}], 'data': {'matchedUser': None}}
