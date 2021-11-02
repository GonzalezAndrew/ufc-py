import requests
from constants import base_url


def get_data(endpoint: str) -> str:
    """
    Returns the data from the endpoint.
    :param endpoint: The endpoint to get the data from.
    :return: The data from the endpoint.
    :rtype: str | None
    """
    data = requests.get(url=f'{base_url}{endpoint}')
    try:
        data.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return ''

    if data.text != '':
        return data.text
    else:
        return ''
