from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

CURRENT_TRACK_ID = "12345"

class TrackUpdate(BaseModel):
    track_id : str

@app.post("/api/current-track")
async def update_track(data:TrackUpdate):
    global CURRENT_TRACK_ID
    CURRENT_TRACK_ID = data.track_id
    return {"status": "ok", "track_id": CURRENT_TRACK_ID}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "track_id" : CURRENT_TRACK_ID
        }
    )