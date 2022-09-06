from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Identity, Integer, SmallInteger, func

from gasoline_prices.database import Base


class Prices(Base):
    __tablename__ = "prices"
    id = Column(Integer, Identity(), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    oil_type_id = Column(SmallInteger, ForeignKey("oil_types.id"), nullable=False)
    survey_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    ref_price = Column(Float, nullable=False)
