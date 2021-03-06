import os

import scrapy
from scrapy.crawler import CrawlerProcess

# taken from https://github.com/ccsucic/MMAData/blob/main/MMAData/UFCScraper/spiders/ufc_spider.py, thanks! :)


class FighterScraper(scrapy.Spider):
    name = 'fighter_scraper'
    start_urls = [
        'http://ufcstats.com/statistics/fighters?char=a&page=all',
        'http://ufcstats.com/statistics/fighters?char=b&page=all',
        'http://ufcstats.com/statistics/fighters?char=c&page=all',
        'http://ufcstats.com/statistics/fighters?char=d&page=all',
        'http://ufcstats.com/statistics/fighters?char=e&page=all',
        'http://ufcstats.com/statistics/fighters?char=f&page=all',
        'http://ufcstats.com/statistics/fighters?char=g&page=all',
        'http://ufcstats.com/statistics/fighters?char=h&page=all',
        'http://ufcstats.com/statistics/fighters?char=i&page=all',
        'http://ufcstats.com/statistics/fighters?char=j&page=all',
        'http://ufcstats.com/statistics/fighters?char=k&page=all',
        'http://ufcstats.com/statistics/fighters?char=l&page=all',
        'http://ufcstats.com/statistics/fighters?char=m&page=all',
        'http://ufcstats.com/statistics/fighters?char=n&page=all',
        'http://ufcstats.com/statistics/fighters?char=o&page=all',
        'http://ufcstats.com/statistics/fighters?char=p&page=all',
        'http://ufcstats.com/statistics/fighters?char=q&page=all',
        'http://ufcstats.com/statistics/fighters?char=r&page=all',
        'http://ufcstats.com/statistics/fighters?char=s&page=all',
        'http://ufcstats.com/statistics/fighters?char=t&page=all',
        'http://ufcstats.com/statistics/fighters?char=u&page=all',
        'http://ufcstats.com/statistics/fighters?char=v&page=all',
        'http://ufcstats.com/statistics/fighters?char=w&page=all',
        'http://ufcstats.com/statistics/fighters?char=x&page=all',
        'http://ufcstats.com/statistics/fighters?char=y&page=all',
        'http://ufcstats.com/statistics/fighters?char=z&page=all',
    ]

    def parse(self, response):
        # Gets the fighter name table
        fighters = response.xpath('//*[@class="b-statistics__table"]//tr')
        # Start rows at 3rd row to skip two header rows
        for row in fighters[2:]:
            # Gets the URL for each fighter page in the fighter name table
            link = row.css('td.b-statistics__table-col a::attr(href)').get()
            # Passes the fighter page URL to a Scrapy Request object for parsing
            yield scrapy.Request(link, callback=self.parse_fighter_page)

    def parse_fighter_page(self, response):

        # Gives fighter wins
        wins = (
            response.css('span.b-content__title-record::text')
            .get()
            .split()[1]
            .split('-')[0]
        )
        # Gives fighter losses
        losses = (
            response.css('span.b-content__title-record::text')
            .get()
            .split()[1]
            .split('-')[1]
        )
        # Gives fighter draws
        draws = (
            response.css('span.b-content__title-record::text')
            .get()
            .split()[1]
            .split('-')[2]
        )
        # Height
        height = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[1]
            .get()
            .strip()
        )
        height = height.replace('"', '')
        if height == '--':
            height = 0
        if isinstance(height, int):
            pass
        else:
            height = height.split("'")
            height = int(height[0]) * 12 + int(height[1])
        # Weight
        weight = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[3]
            .get()
            .strip()
        )
        weight = weight.replace(' lbs', '').replace('.', '')

        # Reach
        reach = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[5]
            .get()
            .strip()
        )
        if reach == '--':
            reach = 0
        else:
            reach = reach.replace('"', '')

        # SLpM
        SLpM = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[11]
            .get()
            .strip()
        )
        # StrAcc
        StrAcc = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[13]
            .get()
            .strip()
        )
        StrAcc = int(StrAcc.replace('%', '')) / 100
        # SApM
        SApM = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[15]
            .get()
            .strip()
        )
        # StrDef
        StrDef = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[17]
            .get()
            .strip()
        )
        StrDef = int(StrDef.replace('%', '')) / 100
        # TDAvg
        TDAvg = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[21]
            .get()
            .strip()
        )
        # TDAcc
        TDAcc = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[23]
            .get()
            .strip()
        )
        TDAcc = int(TDAcc.replace('%', '')) / 100
        # TDDef
        TDDef = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[25]
            .get()
            .strip()
        )
        TDDef = int(TDDef.replace('%', '')) / 100

        # SubAvg
        SubAvg = (
            response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[27]
            .get()
            .strip()
        )

        yield {
            # Gives fighter name on fighter page
            'name': response.css('span.b-content__title-highlight::text').get().strip(),
            # Gives fighter wins
            'wins': int(wins),
            # Gives fighter losses
            'losses': int(losses),
            # Gives fighter draws
            'draws': int(draws),
            # Height
            'height': height,
            # Weight
            'weight': int(weight),
            # Reach
            'reach': int(reach),
            # Stance
            'stance': response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[7]
            .get()
            .strip(),
            # Birthdate
            'dob': response.css(
                'li.b-list__box-list-item.b-list__box-list-item_type_block::text',
            )[9]
            .get()
            .strip(),
            'stats': {
                'SLpM': float(SLpM),
                # StrAcc
                'StrAcc': StrAcc,
                # SApM
                'SApM': float(SApM),
                # StrDef
                'StrDef': StrDef,
                # TDAvg
                'TDAvg': float(TDAvg),
                # TDAcc
                'TDAcc': float(TDAcc),
                # TDDef
                'TDDef': TDDef,
                # SubAvg
                'SubAvg': float(SubAvg),
            },
            'fighter_url': response._url,
        }


# remove old data
if os.path.exists('fighters.json'):
    os.remove('fighters.json')

# set the spider settings
process = CrawlerProcess(
    {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': './data/fighters.json',
    },
)
process.crawl(FighterScraper)

# start the spider
process.start()
