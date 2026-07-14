#!/usr/bin/env python3
"""
Command-line script to search for upcoming events on Meetup.com.

Usage:
    python search_events.py --meetup Hakierspejs-Łodź
    python search_events.py --meetup Hakierspejs-Łodź --regex Radio
    python search_events.py --meetup hakierspejs-lodz
    python search_events.py --city Warsaw
    python search_events.py --city "Krakow" --regex Python
"""

import argparse
import logging
import sys

import meetupscraper


def search_events(meetup_name: str, name_regex: str = None):
    """Search for upcoming events and return results."""
    print(f"Searching events for meetup group: {meetup_name}")
    if name_regex:
        print(f"Filtering by regex: {name_regex}")
    print("-" * 60)

    events = list(meetupscraper.get_upcoming_events(meetup_name, name_regex=name_regex))
    return events


def search_events_by_city(city_name: str, name_regex: str = None, max_groups: int = 10):
    """Search for upcoming events in a city and return results."""
    print(f"Searching events in city: {city_name}")
    if name_regex:
        print(f"Filtering by regex: {name_regex}")
    print(f"Max groups to search: {max_groups}")
    print("-" * 60)

    events = list(meetupscraper.get_events_by_city(city_name, name_regex=name_regex, max_groups=max_groups))
    return events


def print_events(events):
    """Print events in a readable format."""
    if not events:
        print("No events found.")
        return

    print(f"Found {len(events)} events:\n")
    for i, event in enumerate(events, 1):
        print(f"{i}. {event.title}")
        print(f"   URL: {event.url}")
        print(f"   Date: {event.date}")
        if event.venue:
            print(f"   Venue: {event.venue.name}")
            print(f"   Address: {event.venue.street}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Search for upcoming events on Meetup.com by group name or city."
    )
    
    # Create mutually exclusive group for meetup vs city
    search_group = parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument(
        "--meetup", "-m",
        help="Meetup group name or URL slug (e.g., 'Hakierspejs-Łodź' or 'hakierspejs-lodz')",
    )
    search_group.add_argument(
        "--city", "-c",
        help="City name to search for events (e.g., 'Warsaw', 'Krakow')",
    )
    
    parser.add_argument(
        "--regex", "-r",
        help="Filter events by title using a regular expression",
    )
    parser.add_argument(
        "--max-groups",
        type=int,
        default=10,
        help="Maximum number of groups to search when using --city (default: 10)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        if args.city:
            events = search_events_by_city(
                city_name=args.city,
                name_regex=args.regex,
                max_groups=args.max_groups,
            )
        else:
            events = search_events(
                meetup_name=args.meetup,
                name_regex=args.regex,
            )
        print_events(events)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
