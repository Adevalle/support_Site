from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import joinedload
from app.api.track import router as track_router
from app.api.admin import router as admin_router
from app.db.database import SessionLocal,engine
from app.db.models import Base, Track

from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin_router)
app.include_router(track_router)



templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    db: Session = SessionLocal()

    current_track = (
        db.query(Track)
        .filter(Track.is_active == True)
        .first()
    )

    history = (
        db.query(Track)
        .options(joinedload(Track.admin))
        .order_by(Track.added_at.desc())
        .filter(Track.is_active == False)
        .order_by(Track.id.desc())
        .limit(20)
        .all()
    )
    for track in history:
        print(track.admin)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "current_track": current_track,
            "history": history,
        }
    )
