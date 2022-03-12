import unittest
from countries import country_names

# TODO: add meaningful tests

class TestCountries(unittest.TestCase):
    def test_number_of_countries(self):
        self.assertEqual(196, len(country_names))

    def test_first_country(self):
        self.assertEqual('Afghanistan', country_names[0])

    def test_last_country(self):
        self.assertEqual('Zimbabwe', country_names[-1])
