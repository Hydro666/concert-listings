import os
from datetime import datetime
from typing import List, NamedTuple

import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

from scraper.db.models import venue_concert_record
from scraper.db.models import base

URL = 'http://www.foopee.com/punk/the-list/'

CACHED_CSV = '/tmp/records-for-artists.csv'

MONTH_STR_TO_NUM = {
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}


def page_url(num: int) -> str:
    return f'{URL}by-date.{num}.html'


def header_to_datetime(header: str) -> datetime:
    _, month, day = header.split(' ')
    return datetime(2021, MONTH_STR_TO_NUM[month], int(day))

class ShowRecord(NamedTuple):
    venue: str
    artist: str
    time: str
    tail: float


def date_entry_generator(response: requests.Response):
    lines = response.text.split('\n')
    it = iter(lines)
    cur_date = None
    # Go to sections
    for line in it:
        if line == '<UL>':
            break

    while True:

        # Find a section
        for line in it:
            # The presence of a lone '</UL>' when finding a section marks the end of the list.
            if line == '</UL>':
                return
            elt = BeautifulSoup(line, features='html.parser')
            if elt.a.get('name') is not None:
                cur_date = elt.b.string
                break

        # For each entry in the section, yield a row
        for line in it:
            if line == '</UL>':
                break
            row_elt = BeautifulSoup(line, features='html.parser').li
            venue = row_elt.b.a.string
            artists = [tag.string for tag in row_elt.find_all('a')[1:]]
            tail = row_elt.contents[-1]
            for artist in artists:
                yield ShowRecord(venue, artist, header_to_datetime(cur_date), tail)


def main():

    if not os.path.exists(CACHED_CSV):
        print('Cache not found... fetching data')
        records = []
        # Get the pages as tuples.
        for i in range(26):
            response = requests.get(page_url(i))
            records.extend(date_entry_generator(response))

        df = pd.DataFrame.from_records(
            records, columns=['venue', 'artist', 'time', 'tail'])
        df.to_csv('/tmp/records-for-artists.csv', index=False)
    else:
        print('Loading old data')
        df = pd.read_csv(CACHED_CSV)

    # Write to DB.
    secret = os.environ['MYPGPASS']
    engine = create_engine(
        f'postgresql://postgres:{secret}@localhost:5432/foopee', echo=True)
    base.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for _, record in df.iterrows():
        obj = venue_concert_record.VenueConcertRecord(venue=record['venue'],
                                                      artist=record['artist'],
                                                      time=record['time'],
                                                      tail=record['tail'])
        session.add(obj)
    session.commit()


if __name__ == '__main__':
    main()
