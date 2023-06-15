from datetime import datetime

from pydantic import BaseModel


class DataSource(BaseModel):
    title: str
    url: str


class Status(BaseModel):
    last_updated: datetime
    data_source: DataSource
