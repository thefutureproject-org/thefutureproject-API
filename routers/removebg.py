from fastapi import APIRouter, status, UploadFile
from rembg import remove
from fastapi.responses import Response
from .OCR_Modules import image_validate

router = APIRouter(
    prefix="/image",
    tags=["Remove Background from Image"]
)


@router.post("/removebg", status_code=status.HTTP_201_CREATED, summary="Remove background from an image")
async def background_remove(file: UploadFile):
    image_validate.validate_file_size_type(file)
    input = await file.read()
    output = remove(input)
    return Response(content=output, media_type="image/png")
