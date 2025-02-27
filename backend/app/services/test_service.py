from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from uuid import UUID

from ..db.models import Test, Bank, Cycle, Reading, CellValue
from ..schemas.test import TestCreate, TestUpdate, BankCreate, ReadingCreate

class TestService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_test(self, test_data: TestCreate) -> Test:
        """Create a new test record."""
        db_test = Test(**test_data.model_dump())
        self.db.add(db_test)
        await self.db.commit()
        await self.db.refresh(db_test)
        return db_test

    async def get_test(self, test_id: UUID) -> Optional[Test]:
        """Get a test by ID with all related data."""
        query = select(Test).options(
            joinedload(Test.banks).joinedload(Bank.cycles).joinedload(Cycle.readings).joinedload(Reading.cell_values)
        ).where(Test.id == test_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_tests(self, skip: int = 0, limit: int = 100) -> List[Test]:
        """List all tests with pagination."""
        query = select(Test).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_test(self, test_id: UUID, test_data: TestUpdate) -> Optional[Test]:
        """Update a test's status."""
        query = update(Test).where(Test.id == test_id).values(**test_data.model_dump())
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_test(test_id)

    async def create_bank(self, bank_data: BankCreate) -> Bank:
        """Create a new bank for a test."""
        db_bank = Bank(**bank_data.model_dump())
        self.db.add(db_bank)
        await self.db.commit()
        await self.db.refresh(db_bank)
        return db_bank

    async def create_reading(self, reading_data: ReadingCreate, cycle_id: UUID) -> Reading:
        """Create a new reading with cell values."""
        # Create reading
        db_reading = Reading(
            cycle_id=cycle_id,
            reading_number=reading_data.reading_number,
            is_ocv=reading_data.is_ocv
        )
        self.db.add(db_reading)
        await self.db.flush()  # Get the reading ID without committing

        # Create cell values
        cell_values = [
            CellValue(
                reading_id=db_reading.id,
                cell_number=i + 1,
                value=value
            )
            for i, value in enumerate(reading_data.cell_values)
        ]
        self.db.add_all(cell_values)
        await self.db.commit()
        await self.db.refresh(db_reading)
        return db_reading

    async def get_test_by_job_number(self, job_number: str) -> Optional[Test]:
        """Get a test by job number."""
        query = select(Test).where(Test.job_number == job_number)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_bank(self, bank_id: UUID) -> Optional[Bank]:
        """Get a bank by ID with all related data."""
        query = select(Bank).options(
            joinedload(Bank.cycles).joinedload(Cycle.readings).joinedload(Reading.cell_values)
        ).where(Bank.id == bank_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_cycle(self, cycle_id: UUID) -> Optional[Cycle]:
        """Get a cycle by ID with all related data."""
        query = select(Cycle).options(
            joinedload(Cycle.readings).joinedload(Reading.cell_values)
        ).where(Cycle.id == cycle_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_readings_by_cycle(self, cycle_id: UUID) -> List[Reading]:
        """Get all readings for a cycle."""
        query = select(Reading).options(
            joinedload(Reading.cell_values)
        ).where(Reading.cycle_id == cycle_id)
        result = await self.db.execute(query)
        return result.scalars().all() 