from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leetcode, stock_data, ocr, ipinfo, spacebin
from routers import webshot, gfg, morse_code, carbon_code, removebg, codeforces
from routers import github
from contextlib import asynccontextmanager
from routers.Leetcode_Contest import contest_schedule
import json
import fcntl
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routers.Database.mongodb import db_client


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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.close()

app = FastAPI(lifespan=lifespan, title="The Future Project",
              description="Building the foundations of tomorrow with the lightning speed of FastAPI.", version="1.0.0",
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


app.mount("/static", StaticFiles(directory="static"), name="static")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leetcode.router)
app.include_router(gfg.router)
app.include_router(codeforces.router)
app.include_router(github.router)
app.include_router(stock_data.router)
app.include_router(ocr.router)
app.include_router(ipinfo.router)
app.include_router(spacebin.router)
app.include_router(webshot.router)
app.include_router(morse_code.router)
app.include_router(carbon_code.router)
app.include_router(removebg.router)


@app.get("/")
async def main():
    return {"message": "Welcome to The Future Project. Enjoy our services."}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico"

    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        contact=app.contact,
        license_info=app.license_info,
        routes=app.routes,

    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


def get_custom_redoc_html(
    *,
    openapi_url: str,
    title: str,
    redoc_js_url: str = "/static/redoc.standalone.js",
    redoc_favicon_url: str = "/static/favicon.ico",
    with_google_fonts: bool = True
) -> HTMLResponse:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{title}</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """
    if with_google_fonts:
        html += """
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    """
    html += f"""
    <link rel="shortcut icon" href="{redoc_favicon_url}">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {{
        margin: 0;
        padding: 0;
      }}
    </style>
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="{openapi_url}" hide-download-button>
    </redoc>
    <script src="{redoc_js_url}"> </script>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/redoc", include_in_schema=False)
async def redoc_try_it_out() -> HTMLResponse:
    return get_custom_redoc_html(openapi_url=app.openapi_url, title=app.title)
