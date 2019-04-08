# -*- coding: utf-8 -*-

import mock
from redhat.redhat import items
import unittest


class TestSitemapItem(unittest.TestCase):

    def test_class_type(self):
        self.assertTrue(type(items.RedhatItem) is items.scrapy.item.ItemMeta)

    def test_class_supports_fields(self):
        with mock.patch.object(items.scrapy.item, 'Field'):
            a = items.RedhatItem()

        supported_fields = ['loc', 'lastmod']
        for field in supported_fields:
            a[field] = field

        not_supported_fields = ['some', 'random', 'fields']
        for field in not_supported_fields:
            with self.assertRaises(KeyError):
                a[field] = field


if __name__ == '__main__':
    unittest.main()
