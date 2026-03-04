# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import threading

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.core.config import settings
from app.services.oficinas_sync import run_sync

from app.api.routers.auth import router as auth_router
from app.api.routers.oficinas import router as oficinas_router

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("worker")

_lock = threading.Lock()
scheduler = BackgroundScheduler()

def job_sync():
    if not _lock.acquire(blocking=False):
        log.warning("Sync ya está corriendo, saltando esta ejecución.")
        return
    try:
        with SessionLocal() as db:
            result = run_sync(db)
        log.info("Sync OK: %s", result)
    except Exception as e:
        log.exception("Sync FAILED: %s", e)
    finally:
        _lock.release()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    if settings.SCRAPE_ENABLED:
        scheduler.add_job(
            job_sync,
            "interval",
            seconds=settings.SCRAPE_INTERVAL_SECONDS,
            id="abaigroup_sync",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        scheduler.start()
        log.info("Scheduler ON. Interval=%ss", settings.SCRAPE_INTERVAL_SECONDS)

        if settings.SCRAPE_RUN_ON_STARTUP:
            job_sync()

    yield

    if scheduler.running:
        scheduler.shutdown(wait=False)
        log.info("Scheduler OFF.")

app = FastAPI(title="Oficinas API", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(oficinas_router)

@app.get("/health")
def health():
    return {"status": "ok"}