from pydantic import BaseModel, Field

class OficinaCreate(BaseModel):
    pais: str = Field(..., min_length=1, max_length=100)
    ciudad: str = Field(..., min_length=1, max_length=100)
    oficina: str = Field(..., min_length=1, max_length=255)

class OficinaRead(OficinaCreate):
    id: int