#!/usr/bin/env python

"""Tests for `inquisition` package."""
import unittest
from inquisition import inquisition as inq


class TestInquisition(unittest.TestCase):
    def test_get_file_names(self):
        path = 'artifacts/data/king_arthur/*.txt'
        file_list = inq.get_file_names(path)
        self.assertEqual(len(file_list), 15)

    def test_create_title_and_text_schema(self):
        blank_schema = inq.create_title_and_text_schema(analyzer='Stemming')
        self.assertListEqual(blank_schema.names(), ['text', 'title'])


if __name__ == '__main__':
    unittest.main()
