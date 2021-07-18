from typing import List, Type, TypeVar

from scraper import page_parser

T = TypeVar('T')


class DatabaseDriver:
    """Will serve as an interface for interacting with different database
    backends."""
    def write_records(self, records: List[page_parser.ShowRecord]) -> None:
        raise NotImplementedError()

    @classmethod
    def make_driver(cls: Type[T], database_name: str) -> T:
        raise NotImplementedError()
