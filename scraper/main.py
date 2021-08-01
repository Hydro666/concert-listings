from scraper import page_parser
from scraper.db import postgres_driver


def main():
    records = page_parser.get_records()
    # Write to DB.
    driver = postgres_driver.PostgresDriver.make_driver('concerts')
    driver.write_records(records)


if __name__ == '__main__':
    main()
