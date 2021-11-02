from typing import Any
from typing import Dict
from typing import List

from bs4 import BeautifulSoup
from constants import completed_events_url
from constants import upcoming_events_url
from utils import get_data


def _parse(data: str) -> List[Dict[str, Any]]:
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
        find_location = event.find('td', class_='b-statistics__table-col b-statistics__table-col_style_big-top-padding')
        if find_date is not None and find_event is not None:
            event_name = find_event.text.strip()
            event_date = find_date.text.strip()
            event_location = find_location.text.strip()

            parsed_events.append({'Title': event_name, 'Date': event_date, 'Location': event_location})

    return parsed_events


# def all_events(completed_events_data: list, upcoming_events_data: list) -> dict:
#     """
#     Returns all the events.
#     :param completed_events_data: The data from the completed events endpoint.
#     :param upcoming_events_data: The data from the upcoming events endpoint.
#     :return: All the events.
#     :rtype: dict
#     """
#     return {'Events': {'Completed': completed_events, 'Upcoming': upcoming_events}}


# def completed_events() -> dict:
#     """
#     Returns the completed events.
#     :return: The completed events.
#     :rtype: dict
#     """
#     completed_events_data = get_data(completed_events_url)
#     completed_events = _parse(completed_events_data)
#     return {'Completed': completed_events}


# def upcoming_events() -> dict:
#     """
#     Returns the upcoming events.
#     :return: The upcoming events.
#     :rtype: dict
#     """
#     upcoming_events_data = get_data(upcoming_events_url)
#     upcoming_events = _parse(upcoming_events_data)
#     return {'Upcoming': upcoming_events}


class UFCEvents():
    def completed_events(self) -> Dict[str, List[Dict[str, Any]]]:
        completed_events_data = get_data(completed_events_url)
        completed_events = _parse(completed_events_data)
        return {'Completed': completed_events}

    def upcoming_events(self) -> Dict[str, List[Dict[str, Any]]]:
        upcoming_events_data = get_data(upcoming_events_url)
        upcoming_events = _parse(upcoming_events_data)
        return {'Upcoming': upcoming_events}

    def all_events(self) -> Dict[Any, Any]:
        completed_events = self.completed_events()['Completed']
        upcoming_events = self.upcoming_events()['Upcoming']
        return {'Events': {'Completed': completed_events, 'Upcoming': upcoming_events}}
