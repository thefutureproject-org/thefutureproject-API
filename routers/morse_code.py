import morsedecode
from fastapi import APIRouter, UploadFile, HTTPException, status
import schemas

router = APIRouter(
    prefix="/morse_code",
    tags=["Morse Code - Encode and decode morse code online"]
)

FILE_EXTENSIONS = ['py', 'js', 'jsx', 'ts', 'tsx', 'go', 'kt', 'cpp', 'cs', 'c', 'm', 'sql', 'scala', 'hs', 'sh', 'bash', 'ps1', 'php', 'asm',
                   'jl', 'pl', 'cr', 'json', 'yaml', 'toml', 'rs', 'rb', 'java', 'md', 'html', 'xml', 'svg', 'atom', 'rss', 'mathml', 'ssml', 'css', 'txt']


@router.post("/encode/text", status_code=200, summary="Encode text to morse code")
async def morse_code_encode(text: schemas.morse_code_In):
    try:
        return morsedecode.encode(text.text)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid text")


@router.post("/decode/text", status_code=200, summary="Decode morse code to text")
async def morse_code_decode(text: schemas.morse_code_In):
    try:
        return morsedecode.decode(text.text)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid morse code")


@router.post("/encode/file", status_code=200, summary="Encode file to morse code")
async def morse_code_encode_file(file: UploadFile):
    file_extension = file.filename.split(".")[-1]
    if file_extension not in FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")
    contents = await file.read()
    txt = contents.decode()
    try:
        return morsedecode.encode(txt)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid text")


@router.post("/decode/file", status_code=200, summary="Decode morse code to file")
async def morse_code_decode_file(file: UploadFile):
    file_extension = file.filename.split(".")[-1]
    if file_extension not in FILE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file extension")
    contents = await file.read()
    txt = contents.decode()
    try:
        return morsedecode.decode(txt)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid morse code")
