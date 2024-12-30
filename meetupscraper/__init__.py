import urllib.parse
import logging
import dataclasses
import datetime
import re

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


def get_upcoming_events(meetup_name, name_regex=None):
    if ' ' in meetup_name:
        logging.warning('Meetup name contains spaces, replacing with hyphens')
        meetup_name = meetup_name.replace(' ', '-')
    url = f"https://api.meetup.com/{urllib.parse.quote(meetup_name)}/events"
    LOGGER.info("Looking up %r", url)
    r = requests.get(url)

    events = r.json()
    logging.debug("Got events: %r", events)

    if name_regex:
        regex = re.compile(name_regex)
    else:
        regex = None

    for event in events:
        date = datetime.datetime.fromtimestamp(event["time"] / 1000)
        venue = event.get("venue", {"name": "N/A"})

        if regex and not regex.search(event["name"]):
            LOGGER.info("Skipping event %r", event["name"])
            continue

        yield Event(
            title=event["name"],
            date=date,
            url=event["link"],
            venue=Venue(name=venue["name"], street=venue.get("address_1")),
        )
