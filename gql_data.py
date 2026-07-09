from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import json
import requests


def get_gql_data(event_id):
    """Fetch event details from Meetup's GraphQL API."""
    transport = AIOHTTPTransport(url="https://www.meetup.com/gql2")
    
    client = Client(transport=transport)
    
    query = gql("""
    query GetEvent($eventId: ID!) {
      event(id: $eventId) {
        id
        title
        dateTime
        description
        group {
          name
          urlname
        }
        venue {
          address
          city
          lat
          lon
          name
        }
      }
    }
    """)
    
    result = client.execute(query, variable_values={"eventId": str(event_id)})
    
    return result


def geocode_city(city_name):
    """Convert city name to latitude/longitude using Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "meetupscraper/1.0",
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    if not data:
        raise ValueError(f"Could not geocode city: {city_name}")
    
    return float(data[0]["lat"]), float(data[0]["lon"])


def get_groups_by_city(city_name, limit=20):
    """Search for meetup groups in a given city using Meetup's GraphQL API."""
    lat, lon = geocode_city(city_name)
    
    transport = AIOHTTPTransport(url="https://www.meetup.com/gql2")
    
    client = Client(transport=transport)
    
    query = gql("""
    query SearchGroups($query: String!, $first: Int!, $lat: Float!, $lon: Float!) {
      groupSearch(first: $first, filter: {query: $query, lat: $lat, lon: $lon}) {
        edges {
          node {
            id
            name
            urlname
            description
            city
            country
          }
        }
        totalCount
      }
    }
    """)
    
    result = client.execute(query, variable_values={
        "query": city_name,
        "first": limit,
        "lat": lat,
        "lon": lon,
    })
    
    return result
