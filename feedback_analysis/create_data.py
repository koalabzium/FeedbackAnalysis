import pandas as pd
import random


def generate_random_data(passenger_amount):
    data = dict(message=["Hi, I am the feedback message"] * passenger_amount,
                airline_code=[random.randint(0, 5) for i in range(passenger_amount)],
                number_of_fellow_passengers=[random.randint(0, 17) for i in range(passenger_amount)],
                did_receive_compensation=[random.randint(0, 1) for i in range(passenger_amount)])
    data["total_compensation_amount"] = [random.randint(1000, 10000) if data["did_receive_compensation"][i] == 1
                                         else 0 for i in range(passenger_amount)]
    return data


def serialize_tojson(data, file_path):
    df = pd.DataFrame(data)
    df.to_json(file_path)


def serialize_tocsv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path)
