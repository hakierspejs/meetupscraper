import logging
import pprint

import meetupscraper

logging.basicConfig(level=logging.DEBUG)
pprint.pprint(
    list(
        meetupscraper.get_upcoming_events('Hakierspejs-Łodź', name_regex='Radio')
    )
)
