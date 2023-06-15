from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Identity, Integer, SmallInteger, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, relationship

from gasoline_prices.database import Base, async_session
from gasoline_prices.models.oil_types import OilType  # noqa: F401
from gasoline_prices.schemas.prices import PriceCreate, PriceRead, PriceUpdate


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, Identity(), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    oil_type_id = Column(SmallInteger, ForeignKey("oil_types.id"), nullable=False)
    survey_date = Column(Date, nullable=False, index=True)
    price = Column(Integer, nullable=False)
    ref_price = Column(Float, nullable=False)
    oil_type = relationship("OilType")

    def parse_sqlalchemy_object(self):
        if self.oil_type_id:
            del self.oil_type_id
        if self.oil_type:
            self.oil_type_name = self.oil_type.oil_type
            del self.oil_type

    @classmethod
    async def create(self, price: PriceCreate, session: AsyncSession = async_session()):
        async with session.begin():
            try:
                session.add(price)
                await session.flush()
            except Exception:
                return False
            else:
                return True

    @classmethod
    async def read_all(self, session: AsyncSession = async_session()):
        statement = select(self).options(joinedload(self.oil_type))
        result = (await session.execute(statement)).all()
        price_list = []
        if result:
            for r in result:
                r.Price.parse_sqlalchemy_object()
                price_list.append(r.Price)
            return price_list
        else:
            return None

    @classmethod
    async def read_by_type_and_date(self, price: PriceRead, session: AsyncSession = async_session()):
        statement = select(self).where(self.oil_type_id == price.oil_type_id, self.survey_date == price.survey_date)
        result = (await session.execute(statement)).first()
        if result:
            return result.Price
        else:
            return None

    @classmethod
    async def read_by_type_and_range(
        self, oil_type: list, start: datetime, end: datetime, session: AsyncSession = async_session()
    ):
        statement = (
            select(self)
            .where(self.oil_type_id.in_(list(oil_type)), self.survey_date >= start, self.survey_date <= end)
            .options(joinedload(self.oil_type))
        )
        result = (await session.execute(statement)).all()
        price_list = []
        if result:
            for r in result:
                r.Price.parse_sqlalchemy_object()
                price_list.append(r.Price)
            return price_list
        else:
            return None

    async def update(self, price: PriceUpdate, session: AsyncSession) -> None:
        self.updated_at = price.updated_at
        self.oil_type_id = price.oil_type_id
        self.survey_date = price.survey_date
        self.price = price.price
        self.ref_price = price.ref_price
        await session.flush()

    @classmethod
    async def get_latest_updated_at(self, session: AsyncSession = async_session()) -> Optional[datetime]:
        statement = select(self).order_by(desc(self.updated_at)).limit(1)
        result = (await session.execute(statement)).first()
        if result:
            updated_at: datetime = result.Price.updated_at
            updated_at = updated_at.replace(tzinfo=timezone.utc)
            return updated_at
        else:
            return None
