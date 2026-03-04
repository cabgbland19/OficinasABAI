from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.deps import get_db, get_current_user, require_roles
from app.models.oficina import Oficina
from app.schemas.oficina import OficinaCreate, OficinaRead

router = APIRouter(prefix="", tags=["oficinas"])

@router.post("/oficinas", response_model=OficinaRead, status_code=201, dependencies=[Depends(require_roles("admin", "writer"))])
def crear_oficina(payload: OficinaCreate, db: Session = Depends(get_db)):
    oficina = Oficina(**payload.model_dump())
    db.add(oficina)
    try:
        db.commit()
        db.refresh(oficina)
        return oficina
    except IntegrityError:
        db.rollback()
        # ya existe: devolvemos 409 (o puedes devolver el registro existente con 200)
        raise HTTPException(status_code=409, detail="Oficina already exists")

@router.get("/oficinas", response_model=list[OficinaRead], dependencies=[Depends(get_current_user)])
def listar_oficinas(
    pais: str | None = Query(default=None),
    ciudad: str | None = Query(default=None),
    oficina: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Oficina)

    if pais:
        stmt = stmt.where(func.lower(Oficina.pais) == pais.lower())
    if ciudad:
        stmt = stmt.where(func.lower(Oficina.ciudad) == ciudad.lower())
    if oficina:
        stmt = stmt.where(func.lower(Oficina.oficina).contains(oficina.lower()))

    stmt = stmt.offset(offset).limit(limit)
    return db.execute(stmt).scalars().all()