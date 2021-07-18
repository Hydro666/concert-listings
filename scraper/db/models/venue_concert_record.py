from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

from scraper.db.models import base

class VenueConcertRecord(base.Base):
    __tablename__ = 'venue-concert-record'

    id = Column(Integer, primary_key=True)
    venue = Column(String)
    artist = Column(String)
    time = Column(String)
    tail = Column(String, nullable=True)
