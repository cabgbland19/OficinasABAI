import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from app.core.config import settings

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+", re.IGNORECASE)

FOOTER_STOP_RE = re.compile(
    r"(©\s*\d{4})|"
    r"(uso legal)|"
    r"(pol[ií]tica de privacidad)|"
    r"(pol[ií]tica de cookies)|"
    r"(gestionar el consentimiento)|"
    r"(almacenamiento o acceso t[eé]cnico)|"
    r"(cookiedatabase\.org)|"
    r"(siempre activo)|"
    r"(preferencias)|"
    r"(estad[ií]sticas)|"
    r"(marketing)|"
    r"(canal seguridad de la informaci[oó]n)",
    re.IGNORECASE,
)

STOP_INLINE = {"close", "close menu", "oficinas", "sede central"}

@dataclass(frozen=True)
class OficinaScraped:
    pais: str
    ciudad: str
    oficina: str

def _norm(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

def _strip_md_hashes(s: str) -> str:
    return re.sub(r"^\s*#+\s*", "", s).strip()

def _is_country_header(line: str) -> bool:
    clean = _strip_md_hashes(line)
    return clean.lower().startswith("oficinas en ")

def _extract_country(line: str) -> str:
    clean = _strip_md_hashes(line)
    return _norm(clean[len("oficinas en "):])

def _looks_like_city(line: str) -> bool:
    clean = _strip_md_hashes(line)
    low = clean.lower()
    if low.startswith("oficinas en "):
        return False
    if FOOTER_STOP_RE.search(clean):
        return False
    if low in {"contacto", "links", "talento"}:
        return False
    if any(ch.isdigit() for ch in clean):
        return False
    if EMAIL_RE.search(clean):
        return False
    if len(clean) > 60:
        return False
    return True

def scrape_oficinas() -> list[OficinaScraped]:
    r = requests.get(
        settings.SCRAPE_SOURCE_URL,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0 (compatible; oficinas-scraper/1.0)"},
    )
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")
    lines = [_norm(x) for x in soup.get_text("\n").splitlines()]
    lines = [x for x in lines if x]

    oficinas: list[OficinaScraped] = []
    pais = None
    ciudad = None
    buf = []
    in_offices = False

    def flush():
        nonlocal buf
        if pais and ciudad and buf:
            addr = _norm(" ".join(buf))
            if addr and not EMAIL_RE.search(addr) and not FOOTER_STOP_RE.search(addr):
                oficinas.append(OficinaScraped(pais, ciudad, addr))
        buf = []

    for raw in lines:
        clean = _strip_md_hashes(raw)
        low = clean.lower()

        if _is_country_header(clean):
            in_offices = True
            flush()
            pais = _extract_country(clean)
            ciudad = None
            continue

        if not in_offices:
            continue

        if FOOTER_STOP_RE.search(clean) or low in {"contacto", "links", "talento"}:
            flush()
            break

        if low in STOP_INLINE or low.startswith("otras ciudades"):
            flush()
            ciudad = None
            continue

        if EMAIL_RE.search(clean) or low.startswith(("tlf:", "tel:", "+")):
            continue

        if _looks_like_city(clean):
            flush()
            ciudad = clean
            continue

        if ciudad:
            buf.append(clean)

    flush()

    seen = set()
    out = []
    for o in oficinas:
        k = (o.pais.lower(), o.ciudad.lower(), o.oficina.lower())
        if k not in seen:
            seen.add(k)
            out.append(o)
    return out