# tests/conftest.py
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# 1) Env vars ANTES de importar app (por el engine)
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-1234567890"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_PASSWORD"] = "ChangeMe_123!"
os.environ["ADMIN_ROLE"] = "admin"

# 2) Importa app después de setear env
from app.main import app  # noqa: E402

@pytest.fixture(scope="session")
def client():
    # borra la db de tests si existe
    db_file = Path("test.db")
    if db_file.exists():
        db_file.unlink()

    # IMPORTANTÍSIMO: usar context manager para que corra startup/lifespan
    with TestClient(app) as c:
        yield c