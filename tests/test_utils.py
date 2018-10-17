import unittest

from utils import get_date_range


class MyTest(unittest.TestCase):

    def test_get_date_range(self):
        input_1 = {
            'start': '2018-01-01',
            'end': '2018-01-05',
            'fmt': '%Y-%m-%d'
        }

        expected_output_1 = [
            '2018-01-01',
            '2018-01-02',
            '2018-01-03',
            '2018-01-04',
            '2018-01-05'
        ]

        output_1 = get_date_range(**input_1)

        self.assertEqual(output_1, expected_output_1)

        input_2 = {
            'start': '2018-01-01',
            'end': '2018-01-01',
            'fmt': '%Y-%m-%d'
        }

        expected_output_2 = [
            '2018-01-01'
        ]

        output_2 = get_date_range(**input_2)

        self.assertEqual(output_2, expected_output_2)

        input_3 = {
            'start': '2018-01-01',
            'end': '2017-01-01',
            'fmt': '%Y-%m-%d'
        }

        expected_output_3 = []

        output_3 = get_date_range(**input_3)

        self.assertEqual(output_3, expected_output_3)
