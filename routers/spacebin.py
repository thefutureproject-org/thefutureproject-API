import requests
from fastapi import APIRouter, HTTPException, status, UploadFile
import schemas
from config import settings


router = APIRouter(
    prefix="/spacebin",
    tags=["Paste Text Online - SpaceBin"]
)

VALID_EXTENSIONS = ["python", "javascript", "jsx", "typescript", "tsx", "go", "kotlin", "cpp", "csharp", "c", "objc", "sql", "scala", "haskell", "shell-session",
                    "bash", "powershell", "php", "asm6502", "julia", "perl", "crystal", "json", "yaml", "toml", "rust", "ruby", "java", "markdown", "markup", "css"]

FILE_EXTENSIONS_MAPPING = {"py": "python", "js": "javascript", "jsx": "jsx", "ts": "typescript", "tsx": "tsx", "go": "go", "kt": "kotlin", "cpp": "cpp", "cs": "csharp", "c": "c", "m": "objc", "sql": "sql", "scala": "scala", "hs": "haskell", "sh": "shell-session", "bash": "bash", "ps1": "powershell", "php": "php",
                           "asm": "asm6502", "jl": "julia", "pl": "perl", "cr": "crystal", "json": "json", "yaml": "yaml", "toml": "toml", "rs": "rust", "rb": "ruby", "java": "java", "md": "markdown", "html": "markup", "xml": "markup", "svg": "markup", "atom": "markup", "rss": "markup", "mathml": "markup", "ssml": "markup", "css": "css", "txt": "txt"}


async def spacebin_txt(txt: schemas.SpaceBin_txt_In):
    url = "https://spaceb.in/api/v1/documents/"
    payload = {"content": txt.txt, "extension": txt.extension}
    # print(payload)
    response = requests.post(
        url, data=payload, proxies=settings.PROXIES).json()
    # print(response.text)
    id_ = response["payload"]["id"]
    if not id_:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create document")
    return f"https://spaceb.in/{id_}"


@router.post("/text", status_code=status.HTTP_201_CREATED, summary="Paste any text or code")
async def paste_text(txt: schemas.SpaceBin_txt_In):
    if txt.extension != "none" and txt.extension.lower() not in VALID_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid extension")
    return {"url": await spacebin_txt(txt)}


@router.post("/file", status_code=status.HTTP_201_CREATED, summary="Paste a file")
async def paste_file(file: UploadFile):
    file_extension = file.filename.split(".")[1]
    # for ex in VALID_EXTENSIONS:
    #     print(ex)
    if file_extension not in FILE_EXTENSIONS_MAPPING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")
    contents = await file.read()
    txt = contents.decode()
    return {"url": await spacebin_txt(schemas.SpaceBin_txt_In(txt=txt, extension=FILE_EXTENSIONS_MAPPING[file_extension]))}
