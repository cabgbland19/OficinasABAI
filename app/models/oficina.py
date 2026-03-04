from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.models.base import Base

class Oficina(Base):
    __tablename__ = "oficinas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pais: Mapped[str] = mapped_column(String(100), index=True)
    ciudad: Mapped[str] = mapped_column(String(100), index=True)
    oficina: Mapped[str] = mapped_column(String(255))  # dirección