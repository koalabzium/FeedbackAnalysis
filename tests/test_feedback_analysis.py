import unittest
import numpy as np
import pandas as pd
from feedback_analysis import feedback_analysis as fa
import feedback_analysis.create_data as create_data
import os


class TestRead(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        d = dict(message=["Nie", "ma", "wody", "na"],
                 airline_code=[1, 2, 2, 1],
                 number_of_fellow_passengers=[2, 1, 1, 0],
                 did_receive_compensation=[False, np.NaN, True, False],
                 total_compensation_amount=[np.NaN, 2000, 500, 0])
        create_data.serialize_tojson(pd.DataFrame(d), "feedback_analysis/missing_values.json")

    @classmethod
    def tearDownClass(cls):
        os.remove("feedback_analysis/missing_values.json")

    def test_read_file(self):
        with self.assertRaises(ValueError):
            fa.read_file("data.pdf")

    def test_missing_values(self):
        with self.assertRaises(AssertionError):
            fa.read_file("feedback_analysis/missing_values.json")


class TestAnalysis(unittest.TestCase):

    def setUp(self):
        d = dict(message=["Nie", "ma", "wody", "na"],
                 airline_code=[1, 2, 2, 1],
                 number_of_fellow_passengers=[2, 1, 1, 0],
                 did_receive_compensation=[False, True, True, False],
                 total_compensation_amount=[0, 2000, 500, 0])
        self.data = pd.DataFrame(d)

    def test_extract_messages(self):
        result1 = self.data["message"].values.tolist()
        result2 = fa.extract_messages(self.data).values.tolist()
        self.assertEqual(result1, result2)

    def test_average_compensation_per_passenger(self):
        result = fa.calculate_average_compensation_per_passenger(self.data)
        self.assertEqual(625, result)

    def test_most_popular_airline(self):
        result = fa.calculate_most_popular_airline(self.data)
        self.assertEqual([1, 2], result)

    def test_percentage_got_the_compensation(self):
        result = fa.calculate_got_the_compensation_percentage(self.data)
        self.assertEqual(50, result)


class TestSameJsonCsv(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = create_data.generate_random_data(10)
        create_data.serialize_tocsv(data, "feedback_analysis/data.csv")
        create_data.serialize_tojson(data, "feedback_analysis/data.json")
        cls.data_json = fa.read_file("feedback_analysis/data.json")
        cls.data_csv = fa.read_file("feedback_analysis/data.csv")

    @classmethod
    def tearDownClass(cls):
        os.remove("feedback_analysis/data.json")
        os.remove("feedback_analysis/data.csv")

    def test_same_average_compensation_per_passenger(self):
        result_json = fa.calculate_average_compensation_per_passenger(self.data_json)
        result_csv = fa.calculate_average_compensation_per_passenger(self.data_csv)
        self.assertEqual(result_csv, result_json)

    def test_same_most_popular_airline(self):
        result_json = fa.calculate_most_popular_airline(self.data_json)
        result_csv = fa.calculate_most_popular_airline(self.data_csv)
        self.assertEqual(result_csv, result_json)

    def test_same_percentage_got_the_compensation(self):
        result_json = fa.calculate_got_the_compensation_percentage(self.data_json)
        result_csv = fa.calculate_got_the_compensation_percentage(self.data_csv)
        self.assertEqual(result_csv, result_json)


if __name__ == "__main__":
    unittest.main()

