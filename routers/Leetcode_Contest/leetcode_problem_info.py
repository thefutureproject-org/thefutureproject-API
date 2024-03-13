import requests
import concurrent.futures
from config import settings

url = "https://leetcode.com/graphql/"

question_info = {
    "question_id": None,
    "title": None,
    "difficulty": None,
    "category": None,
    "tags": None,
    "description": None
}


def get_topic_tags(title_slug: str):
    payload = {"query": "\n    query singleQuestionTopicTags($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    topicTags {\n      name\n      slug\n    }\n  }\n}\n    ", "variables": {
        "titleSlug": title_slug}, "operationName": "singleQuestionTopicTags"}
    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER).json()
    question_info["tags"] = list(
        map(lambda x: x["name"], response["data"]["question"]["topicTags"]))


def get_description(title_slug: str):
    payload = {"query": "\n    query questionContent($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    content\n    mysqlSchemas\n    dataSchemas\n  }\n}\n    ", "variables": {
        "titleSlug": title_slug}, "operationName": "questionContent"}
    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER).json()

    question_info["description"] = response['data']['question']['content']


def get_title_difficulty_id_category(title_slug: str):
    payload = {"query": "\n    query questionTitle($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    title\n    titleSlug\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    categoryTitle\n  }\n}\n    ", "variables": {
        "titleSlug": title_slug}, "operationName": "questionTitle"}

    response = requests.post(url=url, json=payload,
                             proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER).json()
    question_info["question_id"] = response['data']['question']['questionId']
    question_info["title"] = response['data']['question']['title']
    question_info["difficulty"] = response['data']['question']['difficulty']
    question_info["category"] = response['data']['question']['categoryTitle']


def get_problem_info(title_slug: str):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_topic_tags = executor.submit(get_topic_tags, title_slug)
        future_description = executor.submit(get_description, title_slug)
        future_title_difficulty_id_category = executor.submit(
            get_title_difficulty_id_category, title_slug)
    return question_info
