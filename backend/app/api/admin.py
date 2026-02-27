from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/add")
def add_admin(telegram_id: int, username: str, db: Session = Depends(get_db)):
    admin = Admin(telegram_id=telegram_id, username=username)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@router.get("/get_admin", tags=["admin"])
def get_admin(telegram_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.telegram_id == telegram_id).first()
    if admin:
        return admin
    else:
        raise HTTPException(403, "Admin not found")
