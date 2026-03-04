from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.routers.auth import router as auth_router
from app.api.routers.oficinas import router as oficinas_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Oficinas API (JWT + Roles)", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(oficinas_router)