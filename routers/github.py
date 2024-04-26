from fastapi import APIRouter
import requests
import schemas
from config import settings

router = APIRouter(
    prefix="/github",
    tags=["GitHub"]
)


def is_valid_github_repo(url):
    if not url.startswith("https://github.com/"):
        return False

    parts = url.split("/")
    if len(parts) != 5:
        return False

    username = parts[3]
    repo_name = parts[4]

    api_url = f"https://api.github.com/repos/{username}/{repo_name}"
    response = requests.get(url=api_url, proxies=settings.PROXIES)

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return "Repo Not Found"


@router.post("/repo", status_code=200, summary="Get repository details from GitHub")
async def get_repo_info(repo: schemas.GitHub_Repo_In):
    return is_valid_github_repo(repo.url)
