# -*- coding: utf-8 -*-

import time

from scrapy import item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class RhsitemapItem(item.Item):
    '''Class to represent an item in the sitemap.'''
    loc = item.Field()
    lastmod = item.Field()


class RhsitemapSpider(CrawlSpider):
    name = 'rhsitemap'
    rules = [
        Rule(
            LinkExtractor(
                allow=[
                    r'.*\.html',
                    r'.*\.pdf',
                    r'.*\.xml',
                    r'.*\.txt',
                    r'.*/',
                ],
                deny=[
                    r'.*twitter*',
                    r'.*facebook*'
                ]
            ),
            follow=True, callback='parse_item'
        )
    ]

    def __init__(self, domain='redhat.com', urls='', *args, **kwargs):
        super(RhsitemapSpider, self).__init__(*args, **kwargs)
        self.domain = domain
        self.allowed_domains = [domain]
        self.start_urls = ['http://%s' % domain]
        for url in urls.split(','):
            if not url:
                continue
            self.start_urls.append(url)

    def parse_item(self, response):
        item = RhsitemapItem()
        item['loc'] = response.url

        if 'Last-Modified' in response.headers:
            timestamp = response.headers['Last-Modified']
        else:
            timestamp = response.headers['Date']
        lastmod = time.strptime(timestamp.decode('utf-8'), "%a, %d %b %Y %H:%M:%S %Z")
        item['lastmod'] = time.strftime("%Y-%m-%dT%H:%M:%S%z", lastmod)
        yield item
