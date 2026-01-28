from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.track import router as track_router
from app.storage.track_stage import CURRENT_TRACK

app = FastAPI()
app.include_router(track_router)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "track_id": CURRENT_TRACK["id"],
            "description": CURRENT_TRACK["description"],
            "track_title": CURRENT_TRACK["title"]
        }
    )
