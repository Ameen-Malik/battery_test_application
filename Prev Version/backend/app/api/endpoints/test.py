from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ...db.base import get_db
from ...services.test_service import TestService
from ...schemas.test import (
    TestCreate,
    TestResponse,
    TestUpdate,
    BankCreate,
    BankResponse,
    ReadingCreate,
    ReadingResponse
)

router = APIRouter()

@router.post("/tests", response_model=TestResponse)
async def create_test(
    test_data: TestCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new test."""
    service = TestService(db)
    # Check if job number already exists
    existing_test = await service.get_test_by_job_number(test_data.job_number)
    if existing_test:
        raise HTTPException(status_code=400, detail="Job number already exists")
    return await service.create_test(test_data)

@router.get("/tests", response_model=List[TestResponse])
async def list_tests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: AsyncSession = Depends(get_db)
):
    """List all tests with pagination."""
    service = TestService(db)
    return await service.list_tests(skip=skip, limit=limit)

@router.get("/tests/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific test by ID."""
    service = TestService(db)
    test = await service.get_test(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.patch("/tests/{test_id}", response_model=TestResponse)
async def update_test(
    test_id: UUID,
    test_data: TestUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a test's status."""
    service = TestService(db)
    test = await service.update_test(test_id, test_data)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.post("/banks", response_model=BankResponse)
async def create_bank(
    bank_data: BankCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new bank for a test."""
    service = TestService(db)
    # Verify test exists
    test = await service.get_test(bank_data.test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return await service.create_bank(bank_data)

@router.get("/banks/{bank_id}", response_model=BankResponse)
async def get_bank(
    bank_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific bank by ID."""
    service = TestService(db)
    bank = await service.get_bank(bank_id)
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank

@router.post("/readings", response_model=ReadingResponse)
async def create_reading(
    reading_data: ReadingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new reading for a cycle."""
    service = TestService(db)
    # Verify cycle exists
    cycle = await service.get_cycle(reading_data.cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    return await service.create_reading(reading_data, reading_data.cycle_id)

@router.get("/readings/cycle/{cycle_id}", response_model=List[ReadingResponse])
async def get_cycle_readings(
    cycle_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get all readings for a specific cycle."""
    service = TestService(db)
    # Verify cycle exists
    cycle = await service.get_cycle(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Cycle not found")
    return await service.get_readings_by_cycle(cycle_id) 