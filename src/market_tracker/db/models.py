from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class IntradayPrice(Base):
    __tablename__ = "intraday_prices"

    __table_args__ = (
        UniqueConstraint("ticker", "timestamp", "interval"),
        CheckConstraint("interval in ('minute', 'hour')"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    interval = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    ext_hours = Column(Boolean, default=False)


class DailyPrice(Base):
    __tablename__ = "daily_prices"

    ticker = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    prev_close = Column(Float, nullable=True)
    daily_return = Column(Float, nullable=True)
    ma_7 = Column(Float, nullable=False)
