from sqlalchemy import Column, DateTime, Identity, Integer, String, func

from gasoline_prices.database import Base


class OilType(Base):
    __tablename__ = "oil_types"
    id = Column(Integer, Identity(), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    oil_type = Column(String, nullable=False)
