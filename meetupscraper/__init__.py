import urllib.parse
import logging
import dataclasses
import datetime

import requests


LOGGER = logging.getLogger("meetupscraper")
# logging.basicConfig(level='DEBUG')


@dataclasses.dataclass(frozen=True)
class Venue:
    name: str
    street: str


@dataclasses.dataclass(frozen=True)
class Event:
    url: str
    date: datetime.datetime
    title: str
    venue: Venue


def get_upcoming_events(meetup_name):
    url = f"https://api.meetup.com/2/events?group_urlname={urllib.parse.quote(meetup_name)}"
    LOGGER.info("Looking up %r", url)
    r = requests.get(url)

    events = r.json()["results"]

    for event in events:
        date = datetime.datetime.fromtimestamp(event["time"] / 1000)
        venue = event["venue"]

        yield Event(
            title=event["name"],
            date=date,
            url=event["event_url"],
            venue=Venue(name=venue["name"], street=venue["address_1"]),
        )
