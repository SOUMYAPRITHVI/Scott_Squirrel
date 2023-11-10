# correlation.py

import json
from math import sqrt


def load_journal(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    return data


def compute_phi(journal, event):
    n_11 = n_00 = n_10 = n_01 = n_plus = 0

    for entry in journal:
        if event in entry["events"]:
            x = True
        else:
            x = False

        if "squirrel" in entry["events"]:
            y = True
        else:
            y = False

        n_11 += x and y
        n_00 += not x and not y
        n_10 += x and not y
        n_01 += not x and y

        n_plus += x

    n_10_sqrt = sqrt(n_10)
    n_01_sqrt = sqrt(n_01)
    n_plus_sqrt = sqrt(n_plus)

    phi = (n_11 * n_00 - n_10 * n_01) / (n_10_sqrt * n_01_sqrt * n_plus_sqrt * n_plus)
    return phi


def compute_correlations(file_name):
    journal = load_journal(file_name)
    correlations = {}

    for entry in journal:
        for event in entry["events"]:
            if event not in correlations:
                correlations[event] = compute_phi(journal, event)

    return correlations


def diagnose(file_name):
    correlations = compute_correlations(file_name)

    most_positive = max(correlations, key=correlations.get)
    most_negative = min(correlations, key=correlations.get)

    return most_positive, most_negative
