from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase


class IntradayPrice(DeclarativeBase):
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
