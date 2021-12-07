import json
from typing import Any
from typing import Dict
from typing import List

import requests
from bs4 import BeautifulSoup

completed_events_url = 'http://ufcstats.com/statistics/events/completed?page=all'
upcoming_events_url = 'http://ufcstats.com/statistics/events/upcoming?page=all'


def get_data(url: str) -> str:
    """
    Returns the data from the endpoint.
    :param endpoint: The endpoint to get the data from.
    :return: The data from the endpoint.
    :rtype: str | None
    """
    data = requests.get(url=url)
    try:
        data.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return ''

    if data.text != '':
        return data.text
    else:
        return ''


def _parse(data: str, completed) -> List[Dict[str, Any]]:
    """
    Parses the data from the endpoint.
    :param data: The data from the endpoint.
    :return: The parsed data.
    :rtype: dict
    """
    soup = BeautifulSoup(data, 'html.parser')
    events = soup.find_all('tr', class_='b-statistics__table-row')

    parsed_events = []
    for event in events:
        find_date = event.find('span', class_='b-statistics__date')
        find_event = event.find('a', class_='b-link b-link_style_black')
        find_location = event.find(
            'td',
            class_='b-statistics__table-col b-statistics__table-col_style_big-top-padding',
        )
        if find_date is not None and find_event is not None:
            event_name = find_event.text.strip()
            event_date = find_date.text.strip()
            event_location = find_location.text.strip()

            parsed_events.append(
                {
                    'title': event_name,
                    'date': event_date,
                    'location': event_location,
                    'completed': completed,
                },
            )

    return parsed_events


class UFCEvents:
    def completed_events(self) -> Dict[str, List[Dict[str, Any]]]:
        completed_events_data = get_data(completed_events_url)
        completed_events = _parse(completed_events_data, True)
        return {'completed': completed_events}

    def upcoming_events(self) -> Dict[str, List[Dict[str, Any]]]:
        upcoming_events_data = get_data(upcoming_events_url)
        upcoming_events = _parse(upcoming_events_data, False)
        return {'upcoming': upcoming_events}

    def all_events(self) -> Dict[Any, Any]:
        completed_events = self.completed_events()['completed']
        upcoming_events = self.upcoming_events()['upcoming']
        data = []
        for event in completed_events:
            data.append(event)
        for event in upcoming_events:
            data.append(event)

        return data


all_events = UFCEvents().all_events()
with open('./data/events.json', 'w') as write_file:
    write_file.write(json.dumps(all_events, indent=4))
