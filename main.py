from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leetcode
from contextlib import asynccontextmanager
from routers.Leetcode_Contest import contest_schedule
import json
import fcntl


@asynccontextmanager
async def lifespan(app: FastAPI):
    permission_file = "permission.json"
    with open(permission_file, "r+") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        data = json.load(file)
        if data['permission'] == 'yes':
            data['permission'] = 'no'
            file.seek(0)
            json.dump(data, file)
            file.truncate()
            fcntl.flock(file, fcntl.LOCK_UN)
            contest_schedule.setup_scheduling()
    yield

app = FastAPI(lifespan=lifespan)

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
