"""
Run this once before generating the Phase 3 migration, so Postgres has the
vector type available when Alembic tries to create the `embedding` column.

Usage (from backend/ folder, venv active):
    python database/enable_pgvector.py
"""
from pathlib import Path
import sys

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings

engine = create_engine(settings.database_url)

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    conn.commit()

print("pgvector extension enabled.")
