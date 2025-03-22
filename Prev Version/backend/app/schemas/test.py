from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TestStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class CellType(str, Enum):
    KPL = "KPL"
    KPM = "KPM"
    KPH = "KPH"

# Base schemas
class TestBase(BaseModel):
    job_number: str = Field(..., description="Unique job number for the test")
    customer_name: str = Field(..., description="Name of the customer")
    number_of_cycles: int = Field(..., ge=1, le=5, description="Number of test cycles")
    time_interval: int = Field(..., ge=1, le=2, description="Time interval in hours")

class BankBase(BaseModel):
    bank_number: int = Field(..., ge=1, le=2, description="Bank number (1 or 2)")
    cell_type: CellType
    cell_rate: float = Field(..., gt=0, description="Cell rate in Ah")
    percentage_capacity: float = Field(..., gt=0, le=100, description="Percentage capacity")
    number_of_cells: int = Field(..., ge=10, le=200, description="Number of cells")

    @validator("discharge_current", pre=True, always=True)
    def calculate_discharge_current(cls, v, values):
        if "percentage_capacity" in values and "cell_rate" in values:
            return (values["percentage_capacity"] * values["cell_rate"]) / 100
        return v

class ReadingBase(BaseModel):
    reading_number: int = Field(..., ge=1, description="Reading sequence number")
    is_ocv: bool = Field(..., description="Whether this is an OCV reading")
    cell_values: List[float] = Field(..., description="List of cell voltage readings")

# Create schemas
class TestCreate(TestBase):
    start_date: datetime
    start_time: datetime

class BankCreate(BankBase):
    test_id: UUID4

class ReadingCreate(ReadingBase):
    cycle_id: UUID4

# Response schemas
class CellValueResponse(BaseModel):
    cell_number: int
    value: float

    class Config:
        from_attributes = True

class ReadingResponse(ReadingBase):
    id: UUID4
    timestamp: datetime
    cell_values: List[CellValueResponse]

    class Config:
        from_attributes = True

class CycleResponse(BaseModel):
    id: UUID4
    cycle_number: int
    reading_type: str
    start_time: datetime
    end_time: Optional[datetime]
    duration: Optional[int]
    readings: List[ReadingResponse]

    class Config:
        from_attributes = True

class BankResponse(BankBase):
    id: UUID4
    test_id: UUID4
    discharge_current: float
    cycles: List[CycleResponse]

    class Config:
        from_attributes = True

class TestResponse(TestBase):
    id: UUID4
    status: TestStatus
    created_at: datetime
    banks: List[BankResponse]

    class Config:
        from_attributes = True

# Update schemas
class TestUpdate(BaseModel):
    status: Optional[TestStatus]

class BankUpdate(BaseModel):
    cell_type: Optional[CellType]
    cell_rate: Optional[float]
    percentage_capacity: Optional[float]
    number_of_cells: Optional[int]

class ReadingUpdate(BaseModel):
    cell_values: List[float] 