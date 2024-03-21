from typing import Optional
import requests
from config import settings
from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import Response


router = APIRouter(
    prefix="/carbon",
    tags=["Carbon Code"]
)

api_url = "https://carbonara.solopov.dev/api/cook"

FILE_EXTENSIONS = ['py', 'js', 'jsx', 'ts', 'tsx', 'go', 'kt', 'cpp', 'cs', 'c', 'm', 'sql', 'scala', 'hs', 'sh', 'bash', 'ps1', 'php', 'asm',
                   'jl', 'pl', 'cr', 'json', 'yaml', 'toml', 'rs', 'rb', 'java', 'md', 'html', 'xml', 'svg', 'atom', 'rss', 'mathml', 'ssml', 'css']


@router.get("/themes", status_code=200, summary="Get Themes")
async def get_themes():
    themes = ["Create +", "3024 Night", "A11y Dark", "Blackboard", "Base 16 (Dark)", "Base 16 (Light)", "Cobalt", "Dracula Pro", "Duotone", "Hopscotch", "Lucario", "Material", "Monokai", "Night Owl", "Nord",
              "Oceanic Next", "One Light", "One Dark", "Panda", "Paraiso", "Seti", "Shades of Purple", "Solarized (Dark)", "Solarized (Light)", "SynthWave '84", "Twilight", "Verminal", "VSCode", "Yeti", "Zenburn"]
    return themes


@router.post("/file", status_code=200, summary="Generate Carbon Code from File")
async def generate_carbon_code_from_file(file: UploadFile, backgroundColor: Optional[str] = "#537F7F", theme: Optional[str] = "seti", language: Optional[str] = "auto", font_size: Optional[str] = "14px", fontFamily: Optional[str] = "Hack"):
    file_extension = file.filename.split(".")[-1]
    if file_extension not in FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")
    contents = await file.read()
    code = contents.decode()
    data = {
        "code": code,
        "backgroundColor": backgroundColor,
        "theme": theme,
        "language": language,
        "fontSize": font_size,
        "fontFamily": fontFamily,
        "exportSize": "2x"
    }
    response = requests.post(url=api_url, json=data, proxies=settings.PROXIES)
    return Response(content=response.content, media_type="image/png")


@router.post("/text", status_code=200, summary="Generate Carbon Code from Text")
async def generate_carbon_code_from_text(code: str, backgroundColor: Optional[str] = "#537F7F", theme: Optional[str] = "seti", language: Optional[str] = "auto", font_size: Optional[str] = "14px", fontFamily: Optional[str] = "Hack"):
    data = {
        "code": code,
        "backgroundColor": backgroundColor,
        "theme": theme,
        "language": language,
        "fontSize": font_size,
        "fontFamily": fontFamily,
        "exportSize": "2x"
    }
    response = requests.post(url=api_url, json=data, proxies=settings.PROXIES)
    return Response(content=response.content, media_type="image/png")
