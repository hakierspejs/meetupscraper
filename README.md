# MeetupScraper

A lightweight Python library for scraping upcoming events from [meetup.com](https://meetup.com) groups.

## Features

- Fetch upcoming events for any public Meetup group
- Filter events by name using regular expressions
- Structured event data with title, date, URL, and venue information
- Venue details fetched via Meetup's GraphQL API
- Search events across all groups in a specific city
- Automatic space-to-hyphen conversion for meetup group names
- Handles both datetime and date-only event start times

## Installation

```bash
pip install -e .
```

Or install dependencies manually:

```bash
pip install requests lxml python-dateutil icalendar gql aiohttp
```

## Running the Script

Run the [`search_events.py`](search_events.py) script directly with the desired arguments:

```bash
# Search by meetup group
python search_events.py --meetup Hakierspejs-Łodź --regex Radio

# Search by city
python search_events.py --city Warsaw

# Search by city with regex filter and more groups
python search_events.py --city "Krakow" --regex Python --max-groups 20
```

### CLI Arguments

| Flag | Description | Required |
|------|-------------|----------|
| `--meetup`, `-m` | Meetup group name or URL slug (e.g., `Hakierspejs-Łodź`) | One of `--meetup` or `--city` |
| `--city`, `-c` | City name to search for events (e.g., `Warsaw`, `Krakow`) | One of `--meetup` or `--city` |
| `--regex`, `-r` | Filter events by title using a regular expression | No |
| `--max-groups` | Maximum number of groups to search when using `--city` (default: 10) | No |
| `--debug` | Enable debug logging | No |

## Dependencies

- `requests` — HTTP requests for iCal feed
- `icalendar` — iCal parsing
- `gql` + `aiohttp` — GraphQL client for venue data
- `lxml` — XML/HTML parsing (transitive dependency)
- `python-dateutil` — Date parsing (transitive dependency)

## License

WTFPL
