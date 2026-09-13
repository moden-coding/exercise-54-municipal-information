#!/usr/bin/env python3

import contextlib
import io
import re
import unittest

from src.municipal_information import main

names = [
    "Proportion of pensioners of the population, %",
    "Proportion of the unemployed among the labour force, %",
    "Share of foreign citizens of the population, %",
    "Share of Swedish-speakers of the population, %",
    "Population change from the previous year, %",
    "Population",
    "Region 2018"]


class TestMunicipalInformation(unittest.TestCase):

    def test_first(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        out = buf.getvalue().strip().split("\n")
        self.assertGreaterEqual(len(out), 3, msg="Expected at least three lines of output!")
        line = out[0]
        pattern = r"Shape:\s+(\d+),\s*(\d+).*"
        self.assertRegex(line, pattern, msg="First output line, that should contain the shape, was not in correct form!")
        m = re.match(pattern, line)
        rows = int(m.group(1))
        cols = int(m.group(2))
        self.assertEqual(rows, 490, msg="Incorrect number of rows!")
        self.assertEqual(cols, 7, msg="Incorrect number of columns!")

        line = out[1]
        self.assertEqual("Columns:", line, msg="Incorrect second line!")
        column_names = out[2:]
        self.assertEqual(len(column_names), 7, msg="Expected seven lines of column names!")
        for i, (a, b) in enumerate(zip(names, column_names[::-1])):
            self.assertEqual(a, b, msg="Column name number %i was incorrect!" % i)


if __name__ == '__main__':
    unittest.main()
