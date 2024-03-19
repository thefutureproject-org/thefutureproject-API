import requests
from bs4 import BeautifulSoup
import json
from config import settings
from fastapi import HTTPException, status


def get_problem_data(title_slug: str):
    response = requests.get(
        url=f"https://www.geeksforgeeks.org/problems/{title_slug}/1?page=1&sortBy=submissions", proxies=settings.PROXIES)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        json_data = soup.find('script', id='__NEXT_DATA__').string
        json_data = json.loads(json_data)
        problem_data = json_data['props']['pageProps']['initialState']['problemApi']['queries']
        first_key = next(iter(problem_data))
        first_value = problem_data[first_key]['data']

        proble_details = {
            "id": first_value['id'],
            "problem_name": first_value['problem_name'],
            "difficulty": first_value['difficulty'],
            "marks": first_value['marks'],
            "accuracy": first_value['accuracy'],
            "submissions": first_value['all_submissions'],
            "company_tags": first_value["tags"]["company_tags"],
            "topic_tags": first_value["tags"]["topic_tags"],
            "author": first_value["author"],
            "problem_question": first_value["problem_question"]

        }
        return proble_details
    else:
        get_problem_data(title_slug)
