from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.track import router as track_router


from sqlalchemy.orm import Session
from app.db.database import SessionLocal,engine
from app.db.models import Base, Track
Base.metadata.create_all(bind=engine)

app = FastAPI()
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
        .order_by(Track.added_at.desc())
        .filter(Track.is_active == False)
        .limit(10)
        .all()
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "current_track": current_track,
            "history": history,
        }
    )

'''< h2 > Сегодня
в
эфире: < / h2 >
< p


class ="track-title" > {{track_title}} < / p >

< p


class ="track-canvas" > {{description}} < / p >
'''