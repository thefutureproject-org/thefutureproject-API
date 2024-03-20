from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leetcode, stock_data, ocr, ipinfo, spacebin, webshot, gfg, morse_code
from contextlib import asynccontextmanager
from routers.Leetcode_Contest import contest_schedule
import json
import fcntl
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)


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

app = FastAPI(lifespan=lifespan, title="The Future Project",
              description="Building the foundations of tomorrow with the lightning speed of FastAPI.", version="0.0.1",
              contact={
                  "name": "The Future Project",
                  "url": "https://thefutureproject.tech/",
                  "email": "support@thefutureproject.tech",
              },
              license_info={
                  "name": "GNU Affero General Public License v3.0",
                  "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"
              },
              redoc_url=None, docs_url=None)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leetcode.router)
app.include_router(stock_data.router)
app.include_router(ocr.router)
app.include_router(ipinfo.router)
app.include_router(spacebin.router)
app.include_router(webshot.router)
app.include_router(gfg.router)
app.include_router(morse_code.router)


@app.get("/")
async def main():
    return {"message": "Welcome to The Future Project"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title,
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js"
    )
