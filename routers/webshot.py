from htmlwebshot import WebShot
import secrets
import string
from fastapi import APIRouter, HTTPException, status, UploadFile
import schemas
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os

router = APIRouter(
    prefix="/webshot",
    tags=["Webshot - Take a screenshot of a website or text online"]
)

FILE_EXTENSIONS = ['py', 'js', 'jsx', 'ts', 'tsx', 'go', 'kt', 'cpp', 'cs', 'c', 'm', 'sql', 'scala', 'hs', 'sh', 'bash', 'ps1', 'php', 'asm',
                   'jl', 'pl', 'cr', 'json', 'yaml', 'toml', 'rs', 'rb', 'java', 'md', 'html', 'xml', 'svg', 'atom', 'rss', 'mathml', 'ssml', 'css', 'txt']


def cleanup(file_path):
    os.remove(file_path)


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def take_webshot_url(url, size, quality, delay, flags, params):
    shot_url = WebShot()
    if size is not None:
        shot_url.size = size
    if quality is not None:
        shot_url.quality = quality
    if delay is not None:
        shot_url.delay = delay
    if flags is not None:
        shot_url.flags = flags
    if params is not None:
        shot_url.params = params
    fn = f'{generate_random_string(20)}.png'
    path = await shot_url.create_pic_async(url=url, output=fn)
    return path


async def take_webshot_file(text: str):
    shot_file = WebShot()
    shot_file.quality = 100
    filename = f'{generate_random_string(20)}.png'
    path = await shot_file.create_pic_async(other=text, output=filename)
    return path


@router.post("/url", status_code=status.HTTP_201_CREATED, summary="Take a screenshot of a website")
async def take_webshot_from_url(url: schemas.Webshot_Url_In):
    if url.flags is None:
        url.flags = []
    if "--enable-javascript" not in url.flags:
        url.flags.append("--enable-javascript")

    if "--disable-smart-width" not in url.flags:
        url.flags.append("--disable-smart-width")
    file_path = await take_webshot_url(
        url.url, url.size, url.quality, url.delay, url.flags, url.params)
    return FileResponse(path=file_path, media_type="image/png", background=BackgroundTask(cleanup, file_path))


@router.post("/text", status_code=status.HTTP_201_CREATED, summary="Take a screenshot of a text")
async def take_webshot_from_text(file: UploadFile):
    file_extension = file.filename.split(".")[-1]
    if file_extension not in FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")
    contents = await file.read()
    txt = contents.decode()
    file_path = await take_webshot_file(txt)
    return FileResponse(path=file_path, media_type="image/png", background=BackgroundTask(cleanup, file_path))
