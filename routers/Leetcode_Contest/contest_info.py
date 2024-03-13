import requests
import concurrent.futures
from config import settings


def get_problem_info(title_slug: str, result: dict, index: str, contest_name: str):

    leetCodeData = {"operationName": "questionData", "variables": {"titleSlug": title_slug}, "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
    req = requests.post('https://leetcode.com/graphql/',
                        json=leetCodeData, proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER).json()
    # print(req.text)
    leetCodeTitle = req['data']['question']['title']
    Problemdifficulty = req['data']['question']['difficulty']
    Topictag = req['data']['question']['topicTags']

    result["problems"][index]["name"] = leetCodeTitle
    result["problems"][index][
        "contest_problem_link"] = f"https://leetcode.com/contest/{contest_name}/problems/{title_slug}/"
    result["problems"][index][
        "problemset_problem_link"] = f"https://leetcode.com/problems/{title_slug}/"
    result["problems"][index]["tags"] = [tag["name"]
                                         for tag in Topictag]
    result["problems"][index]["difficulty"] = Problemdifficulty


def contest_info(contest_name: str):
    response = requests.get(
        f"https://leetcode.com/contest/api/info/{contest_name}/", proxies=settings.PROXIES, headers=settings.LEETCODE_HEADER).json()

    # print(response.text)
    indexes = ['A', 'B', 'C', 'D']
    titleSlugs = [question['title_slug'] for question in response['questions']]

    result = {
        "contest_name": response["contest"]["title"],
        "contest_link": f"https://leetcode.com/contest/{contest_name}/",
        "problems": {
            "A": {"name": "", "contest_problem_link": "", "problemset_problem_link": "", "tags": "", "difficulty": ""},
            "B": {"name": "", "contest_problem_link": "", "problemset_problem_link": "", "tags": "", "difficulty": ""},
            "C": {"name": "", "contest_problem_link": "", "problemset_problem_link": "", "tags": "", "difficulty": ""},
            "D": {"name": "", "contest_problem_link": "", "problemset_problem_link": "", "tags": "", "difficulty": ""},
        }
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_problem_info, title_slug, result, index, contest_name)
                   for index, title_slug in zip(indexes, titleSlugs)]

    return result


# print(contest_info("biweekly-contest-123"))
