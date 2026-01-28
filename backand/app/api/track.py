from fastapi import APIRouter, HTTPException
from app.models.track import Track
from app.services.yandex_parser import parse_track_id, fetch_track_metadata
from app.storage.track_stage import CURRENT_TRACK

router = APIRouter(prefix="/api", tags=["track"])

# Глобальная переменная трека в памяти
@router.get("/current-track")
async def get_track_id():
    return CURRENT_TRACK

@router.post("/current-track")
async def set_track(payload: Track):
    try:
        track_id = parse_track_id(payload.url)
        metadata = fetch_track_metadata(payload.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    CURRENT_TRACK["id"] = track_id
    CURRENT_TRACK["title"] = metadata["title"]
    CURRENT_TRACK["description"] = metadata["description"]
    CURRENT_TRACK["cover"] = metadata["cover"]

    return CURRENT_TRACK
# async def update_track(payload: TrackCreate):
#     global CURRENT_TRACK_ID
#     if not data.track_id:
#         raise HTTPException(status_code=400, detail="track_id is required")
#
#     CURRENT_TRACK_ID = data.track_id
#     try:
#         save_state(CURRENT_TRACK_ID)
#     except Exception as e:
#         print("Exception api:", e)
#         raise HTTPException(status_code=500, detail="exception save track")
#
#     return {"status": "ok", "track_id": CURRENT_TRACK_ID}

