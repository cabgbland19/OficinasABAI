from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.base import Base
from app.db.session import engine
from app.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash

def init_db() -> None:
    # asegurar folder si es sqlite file
    if settings.database_url.startswith("sqlite:///./"):
        Path("./data").mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        stmt = select(User).where(User.username == settings.admin_username)
        existing = db.execute(stmt).scalar_one_or_none()
        if existing is None:
            admin = User(
                username=settings.admin_username,
                hashed_password=get_password_hash(settings.admin_password),
                role=settings.admin_role,
                is_active=True,
            )
            db.add(admin)
            db.commit()