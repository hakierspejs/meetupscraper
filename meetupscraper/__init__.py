import urllib.parse
import logging
import dataclasses
import datetime
import re
from datetime import timezone
import icalendar
import requests
from gql_data import get_gql_data, get_groups_by_city
import json


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
    url = f"https://meetup.com/{urllib.parse.quote(meetup_name)}/events/ical"
    LOGGER.info("Looking up %r", url)
    r = requests.get(url)

    # Parse iCal data
    cal = icalendar.Calendar.from_ical(r.content)
    logging.debug("Got iCal data")

    if name_regex:
        regex = re.compile(name_regex)
    else:
        regex = None

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        event_name = str(component.get('summary', 'No Title'))
        event_url = str(component.get('url', ''))
        
        dtstart = component.get('dtstart')
        event_start = dtstart.dt
        
        if isinstance(event_start, datetime.date) and not isinstance(event_start, datetime.datetime):
            event_start = datetime.datetime.combine(event_start, datetime.time.min)

        if regex and not regex.search(event_name):
            LOGGER.info("Skipping event %r", event_name)
            continue

        try:
            event_id = re.search(r".+\/(\d+)\/", event_url).groups()[0]
            gql_data = get_gql_data(event_id)
            venue = Venue(
                    name=gql_data['event']['venue']['name'],
                    street=gql_data['event']['venue']['address'] + ', ' + gql_data['event']['venue']['city']
            )
        except:
            venue = None

        yield Event(
            title=event_name,
            date=event_start,
            url=event_url,
            venue=venue,
        )


def get_events_by_city(city_name, name_regex=None, max_groups=10):
    """
    Search for upcoming events in a given city by finding groups and aggregating their events.
    
    Args:
        city_name: Name of the city to search for events (e.g., 'Warsaw', 'Krakow')
        name_regex: Optional regex pattern to filter events by title
        max_groups: Maximum number of groups to search (default 10)
    
    Yields:
        Event objects for all upcoming events in the city
    """
    LOGGER.info("Searching for groups in city: %s", city_name)
    
    # Search for groups in the city
    groups_result = get_groups_by_city(city_name, limit=max_groups)
    
    groups = groups_result.get('groupSearch', {}).get('edges', [])
    if not groups:
        LOGGER.warning("No groups found for city: %s", city_name)
        return
    
    LOGGER.info("Found %d groups in %s", len(groups), city_name)
    
    # Collect events from all groups
    seen_events = set()  # To avoid duplicates
    
    for group_edge in groups:
        group = group_edge.get('node', {})
        urlname = group.get('urlname')
        
        if not urlname:
            continue
            
        LOGGER.info("Fetching events from group: %s", group.get('name', urlname))
        
        try:
            for event in get_upcoming_events(urlname, name_regex=name_regex):
                # Use URL as unique identifier to avoid duplicates
                if event.url not in seen_events:
                    seen_events.add(event.url)
                    yield event
        except Exception as e:
            LOGGER.warning("Failed to fetch events from group %s: %s", urlname, e)
            continue
