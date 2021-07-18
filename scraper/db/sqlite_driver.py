from typing import List, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraper import page_parser
from scraper.db import driver
from scraper.db.models import base
from scraper.db.models import venue_concert_record

T = TypeVar('T')


def _db_file_path(database_name: str) -> str:
    return f'sqlite:////tmp/{database_name}.db'


class SQLiteDriver(driver.DatabaseDriver):
    def __init__(self, connection_string: str):
        self._engine = create_engine(connection_string)
        self._session_maker = sessionmaker(bind=self._engine)
        base.Base.metadata.create_all(self._engine)

    def write_records(self, records: List[page_parser.ShowRecord]) -> None:
        venue_concert_record.VenueConcertRecord.__table__.drop(
            bind=self._engine)
        venue_concert_record.VenueConcertRecord.__table__.create(
            bind=self._engine)
        with self._session_maker() as session:
            for record in records:
                elt = venue_concert_record.VenueConcertRecord(
                    venue=record.venue,
                    artist=record.artist,
                    time=record.time,
                    tail=record.tail)
                session.add(elt)
            session.commit()

    @classmethod
    def make_driver(cls: Type[T], database_name: str) -> T:
        return cls(_db_file_path(database_name))
