from datetime import date, datetime

from pydantic import BaseModel


class PriceSelect(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    oil_type_id: int
    survey_date: date
    price: int
    ref_price: float

    class Config:
        orm_mode = True


class PriceCreate(BaseModel):
    created_at: datetime
    updated_at: datetime
    oil_type_id: int
    survey_date: date
    price: int
    ref_price: float
