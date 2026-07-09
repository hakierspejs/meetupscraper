import requests
import json
import sys

url = 'https://www.meetup.com/gql2'

# Try different approaches
queries = [
    ("groupSearch with query only", """
    query {
      groupSearch(first: 10, filter: {query: "Warsaw", lat: 52.2297, lon: 21.0122}) {
        edges {
          node {
            name
            urlname
            city
            country
          }
        }
        totalCount
      }
    }
    """),
    ("groupSearch with country", """
    query {
      groupSearch(first: 10, filter: {country: "PL", query: "", lat: 52.2297, lon: 21.0122}) {
        edges {
          node {
            name
            urlname
            city
            country
          }
        }
        totalCount
      }
    }
    """),
    ("groupSearch with radius", """
    query {
      groupSearch(first: 10, filter: {city: "Warsaw", query: "", lat: 52.2297, lon: 21.0122, radius: 50}) {
        edges {
          node {
            name
            urlname
            city
            country
          }
        }
        totalCount
      }
    }
    """),
    ("groups all", """
    query {
      groups(where: {first: 10}) {
        name
        urlname
        city
        country
      }
    }
    """),
]

with open('test_results.txt', 'w', encoding='utf-8') as f:
    for name, query in queries:
        response = requests.post(url, json={'query': query})
        f.write(f"=== {name} ===\n")
        f.write(f"Status: {response.status_code}\n")
        f.write(f"Body: {response.text[:1200]}\n\n")

print("done")
