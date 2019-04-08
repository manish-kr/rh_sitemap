# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

import lxml
import scrapy
from scrapy import exporters


class SitemapItemExporter(exporters.XmlItemExporter):
    '''XmlItemExporer with adjusted attributes for the root element.'''

    def start_exporting(self):
        '''Set namespace / schema attributes for the root element.'''
        self.xg.startDocument()
        self.xg.startElement(self.root_element, {
            "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation":
            "http://www.sitemaps.org/schemas/sitemap/0.9 "
            "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
        })


class IgnoreDuplicateUrls(object):
    '''Ignore duplicated URLs.'''

    def __init__(self):
        self.processed = set()

    def process_item(self, item, spider):
        '''Check if a URL was already found.'''
        if item['loc'] in self.processed:
            raise scrapy.exceptions.DropItem("Duplicate URL found: %s." % item['loc'])
        else:
            self.processed.add(item['loc'])
            return item


class ExportSitemap(object):
    '''Write found URLs to a sitemap file.'''

    def __init__(self):
        self.files = {}
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, scrapy.signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, scrapy.signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        output = open(os.path.join(os.getcwd(), 'sitemap_%s.xml' % spider.domain), 'w')
        self.files[spider] = output
        self.exporter = SitemapItemExporter(output, item_element='url', root_element='urlset')
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        output = self.files.pop(spider)
        output.close()
        tree = lxml.etree.parse(os.path.join(os.getcwd(), "sitemap_%s.xml" % spider.domain))
        with open(os.path.join(os.getcwd(), "sitemap_%s.xml" % spider.domain), 'w') as pretty:
            pretty.write("<?xml-stylesheet type='text/xsl' href='xml-sitemap.xsl'?>\n")
            pretty.write(lxml.etree.tostring(tree, pretty_print=True).decode('utf-8'))

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
