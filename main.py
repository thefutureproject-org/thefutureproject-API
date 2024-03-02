from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leetcode
from contextlib import asynccontextmanager

from routers.Leetcode_Contest import contest_schedule

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup the scheduler on startup
    contest_schedule.setup_scheduling()
    yield


@app.get("/")
async def main():
    return {"message": "The Future Project"}

app.lifespan = lifespan
