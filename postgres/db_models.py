from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IntradayPrice(Base):
    __tablename__ = 'intraday_prices'

    __table_args__ = (
        UniqueConstraint('ticker', 'timestamp'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    ext_hours = Column(Boolean, default=False)
