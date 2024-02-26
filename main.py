from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leetcode


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leetcode.router)


@app.get("/")
async def main():
    return {"message": "The Future Project"}
