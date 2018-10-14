import unittest
import numpy as np
import pandas as pd
import feedback_analysis as fa


class TestRead(unittest.TestCase):

    def test_read_file(self):
        with self.assertRaises(ValueError):
            fa.read_file("data.pdf")


class TestAnalyse(unittest.TestCase):

    def setUp(self):
        d = dict(message=["Nie", "ma", "wody", "na"],
                 airline_code=[1, 2, 2, 1],
                 number_of_fellow_passengers=[2, 1, 1, 0],
                 did_receive_compensation=[False, True, True, False],
                 total_compensation_amount=[np.NaN, 2000, 500, np.NaN])
        self.data = pd.DataFrame(d)

    def test_average_compensation_per_passenger(self):
        result = fa.calculate_average_compensation_per_passenger(self.data)
        self.assertEqual(625, result)

    def test_most_popular_airline(self):
        result = fa.calculate_most_popular_airline(self.data)
        self.assertEqual([1,2], result)

    def test_percentage_got_the_compensation(self):
        result = fa.calculate_got_the_compensation_percentage(self.data)
        self.assertEqual(50, result)


if __name__ == '__main__':
    unittest.main()

