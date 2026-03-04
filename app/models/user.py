from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="reader")  # admin|writer|reader
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)