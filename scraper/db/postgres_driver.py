import os
from typing import List, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scraper import page_parser
from scraper.db import driver
from scraper.db.models import base
from scraper.db.models import venue_concert_record

T = TypeVar('T')

PG_PASSWORD_VARIABLE = 'MYPGPASS'


class PostgresDriver(driver.DatabaseDriver):
    def __init__(self, database: str, user: str, password: str):
        connection_string = f'postgresql://{user}:{password}@localhost:5432/{database}'
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

        if PG_PASSWORD_VARIABLE not in os.environ:
            raise ValueError('Uh oh freako')
        return cls(database_name, 'postgres', os.environ[PG_PASSWORD_VARIABLE])
