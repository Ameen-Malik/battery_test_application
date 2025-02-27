import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from alembic.config import Config
from alembic import command
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.config import settings
from backend.app.db.base import Base

async def init_db():
    """Initialize the database."""
    # Create async engine
    engine = create_async_engine(settings.DATABASE_URL)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Run Alembic migrations
    alembic_cfg = Config("backend/alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    asyncio.run(init_db()) 