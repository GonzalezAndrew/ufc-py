'''
# change this to grab the href in the a tag to parse the fighters fight stats
<td class="b-statistics__table-col">
    <a href="http://ufcstats.com/fighter-details/c9f6385af6df66d7" class="b-link b-link_style_black">Papy</a>
</td>
<td class="b-statistics__table-col">
    <a href="http://ufcstats.com/fighter-details/c9f6385af6df66d7" class="b-link b-link_style_black">Abedi</a>
</td>
<td class="b-statistics__table-col">
    <a href="http://ufcstats.com/fighter-details/c9f6385af6df66d7" class="b-link b-link_style_black">Makambo</a>
</td>

'''
from bs4 import BeautifulSoup
from constants import fighters_urls
from utils import get_data


for url in fighters_urls:
    data = get_data(url)
    soup = BeautifulSoup(data, 'html.parser')

    data = soup.find_all('table', class_='b-statistics__table')

    table_data = soup.table.find_all('tr')
    for entry in table_data[1:]:
        if len(entry.find_all('a', class_='b-link b-link_style_black')) > 0:
            first_name = entry.find_all('a', class_='b-link b-link_style_black')[0].text.strip()
            last_name = entry.find_all('a', class_='b-link b-link_style_black')[1].text.strip()
            nick_name = entry.find_all('a', class_='b-link b-link_style_black')[2].text.strip()
            if len(nick_name) == 0:
                nick_name = 'None'

            height = entry.find_all('td', class_='b-statistics__table-col')[3].text.strip()
            weight = entry.find_all('td', class_='b-statistics__table-col')[4].text.strip()
            reach = entry.find_all('td', class_='b-statistics__table-col')[5].text.strip()
            stance = entry.find_all('td', class_='b-statistics__table-col')[6].text.strip()
            wins = entry.find_all('td', class_='b-statistics__table-col')[7].text.strip()
            losses = entry.find_all('td', class_='b-statistics__table-col')[8].text.strip()
            draws = entry.find_all('td', class_='b-statistics__table-col')[9].text.strip()
            belts = entry.find_all('td', class_='b-statistics__table-col')[10]
            if len(belts) > 0:
                belt = entry.find('img', class_='b-list__icon')
                if belt is not None:
                    belt = 'True'
                else:
                    belt = 'False'
            print(first_name, last_name, nick_name, height, weight, reach, stance, wins, losses, draws, belt)
