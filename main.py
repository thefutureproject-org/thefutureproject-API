from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leetcode
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import Depends
from routers.Database.database import get_db
from routers.Leetcode_Contest import contest_schedule


@asynccontextmanager
async def lifespan(app: FastAPI, db: Session = Depends(get_db)):
    # Setup the scheduler on startup
    contest_schedule.setup_scheduling(db)
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
