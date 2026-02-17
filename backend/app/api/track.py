from fastapi import APIRouter, HTTPException, Depends
from app.services.yandex_parser import parse_track_id, fetch_track_metadata

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Track
from app.models.track import TrackCreate, TrackOut

router = APIRouter(prefix="/api/tracks", tags=["tracks"])
@router.post("/current", response_model=TrackOut)
def set_current_track(payload: TrackCreate, db: Session = Depends(get_db)):
    track_id = parse_track_id(payload.url)

    # Снимаем текущий трек
    db.query(Track).filter(Track.is_active == True).update(
        {"is_active": False}
    )

    track = Track(
        url=payload.url,
        yandex_track_id=track_id,
        is_active=True
    )

    db.add(track)
    db.commit()
    db.refresh(track)

    return track

@router.get("/current", response_model=TrackOut)
def get_current_track(db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.is_active == True).first()

    if not track:
        raise HTTPException(status_code=404, detail="No active track")

    return track

@router.get("/history", response_model=list[TrackOut])
def get_track_history(db: Session = Depends(get_db)):
    return (
        db.query(Track)
        .order_by(Track.added_at.desc())
        .all()
    )

# @router.post("/current-track")
# async def set_track(payload: Track):
#     try:
#         track_id = parse_track_id(payload.url)
#         # metadata = fetch_track_metadata(payload.url)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#     CURRENT_TRACK["id"] = track_id
#     # CURRENT_TRACK["title"] = metadata["title"]
#     # CURRENT_TRACK["description"] = metadata["description"]
#
#     return CURRENT_TRACK
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

