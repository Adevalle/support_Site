from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.state import load_state, save_state

router = APIRouter(prefix="/api", tags=["track"])

# Глобальная переменная трека в памяти
state = load_state()
CURRENT_TRACK_ID = state.get("current_track_id", "123456")

class TrackUpdate(BaseModel):
    track_id: str

@router.get("/current-track")
async def get_track_id():
    return {"track_id": CURRENT_TRACK_ID}

@router.post("/current-track")
async def update_track(data: TrackUpdate):
    global CURRENT_TRACK_ID
    if not data.track_id:
        raise HTTPException(status_code=400, detail="track_id is required")

    CURRENT_TRACK_ID = data.track_id
    try:
        save_state(CURRENT_TRACK_ID)
    except Exception as e:
        print("Exception api:", e)
        raise HTTPException(status_code=500, detail="exception save track")

    return {"status": "ok", "track_id": CURRENT_TRACK_ID}