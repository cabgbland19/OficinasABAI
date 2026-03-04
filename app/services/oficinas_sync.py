import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.oficina import Oficina
from app.services.abai_scrapper import scrape_oficinas

log = logging.getLogger("worker")

def run_sync(db: Session) -> dict:
    scraped = scrape_oficinas()
    created = 0
    skipped = 0

    for o in scraped:
        row = Oficina(pais=o.pais, ciudad=o.ciudad, oficina=o.oficina)
        db.add(row)
        try:
            db.commit()
            created += 1
        except IntegrityError:
            db.rollback()
            skipped += 1

    return {"scraped": len(scraped), "created": created, "skipped": skipped}