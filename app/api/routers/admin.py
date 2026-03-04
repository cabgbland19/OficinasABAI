from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_roles
from app.services.oficinas_sync import run_sync

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/scrape/run", dependencies=[Depends(require_roles("admin"))])
def run_scrape(db: Session = Depends(get_db)):
    return run_sync(db)