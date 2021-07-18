from scraper import page_parser
from scraper.db import sqlite_driver


def main():
    records = page_parser.get_records()
    # Write to DB.
    driver = sqlite_driver.SQLiteDriver.make_driver('foopee')
    driver.write_records(records)


if __name__ == '__main__':
    main()
