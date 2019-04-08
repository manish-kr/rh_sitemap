# -*- coding: utf-8 -*-

from redhat.redhat.spiders import rhsitemap
import unittest


class TestSitemapSpider(unittest.TestCase):

    def setUp(self):
        self.spider = rhsitemap.RhsitemapSpider()

    def test_set_vars_on_init(self):
        domain = 'redhat.com'
        self.assertEqual(self.spider.domain, domain)
        self.assertEqual(self.spider.allowed_domains, [domain])
        self.assertEqual(self.spider.start_urls, ['http://%s' % domain])

    def test_start_urls_get_appended(self):
        urls = 'new.redhat.com, old.redhat.com'
        urls_len = len(urls.split(','))
        spider_len = len(self.spider.start_urls)

        spider_with_urls = rhsitemap.RhsitemapSpider(urls=urls)
        spider_with_urls_len = len(spider_with_urls.start_urls)

        self.assertEqual(spider_with_urls_len, (urls_len + spider_len))


if __name__ == '__main__':
    unittest.main()
