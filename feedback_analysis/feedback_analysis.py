import pandas as pd
import matplotlib as plt
import numpy as np
import engarde.decorators as ed
import engarde.checks as ec


@ed.has_dtypes(items=dict(number_of_fellow_passengers=int, did_receive_compensation=int))
def read_file(file_path):
    if file_path.lower().endswith(".json"):
        feedback = pd.read_json(file_path)
        ec.is_shape(feedback, (-1, 5))
    elif file_path.lower().endswith(".csv"):
        feedback = pd.read_csv(file_path)
        ec.is_shape(feedback, (-1, 6))
    else:
        raise ValueError("This file format is not supported yet.")
    return feedback


def extract_messages(feedback):
    messages = feedback["message"]
    return messages


def plot_distribution_fellow_passengers(feedback):
    feedback.plot(y='number_of_fellow_passengers', kind="hist")
    plt.pyplot.show()


def calculate_average_compensation_per_passenger(feedback):
    return (feedback["total_compensation_amount"] /
            (feedback["number_of_fellow_passengers"] + 1)).mean()


def calculate_got_the_compensation_percentage(feedback):
    return np.count_nonzero(feedback['did_receive_compensation']) \
           / len(feedback['did_receive_compensation']) * 100


def calculate_most_popular_airline(feedback):
    most_popular = feedback["airline_code"].mode()
    return most_popular.tolist()


data = read_file('feedback_analysis/data.json')
data2 = read_file('feedback_analysis/data.csv')

print(calculate_most_popular_airline(data))
print(extract_message(data))
print(calculate_most_popular_airline(data2))
