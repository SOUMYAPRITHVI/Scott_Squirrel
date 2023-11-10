import json
from math import sqrt
FILE_NAME="journal.json"

def load_journal(FILE_NAME):
    with open(FILE_NAME, 'r') as file:
        data = json.load(file)
    return data

def compute_phi(journal, event):
    journal1 = load_journal(journal)
    n_11 = n_00 = n_10 = n_01 = n_1plus = n_0plus = n_plus1 = n_plus0 = 0
    for entry in journal1:
        if event in entry['events']:
            x = True
            n_1plus += x
        else:
            x = False
            n_0plus += 1
        if entry['squirrel']:
            y = True
            n_plus1 += y

        else:
            y = False
            n_plus0 += 1

        n_11 += x and y
        n_00 += not x and not y
        n_10 += x and not y
        n_01 += not x and y

    phi = (n_11 * n_00 - n_10 * n_01) / sqrt(n_1plus* n_0plus * n_plus1 * n_plus0)
    return phi
def compute_correlations(journal):
    journal1 = load_journal(journal)
    correlations = {}

    for entry in journal1:
        for event in entry['events']:
            if event not in correlations:
                correlations[event] = compute_phi(journal, event)
    return correlations
def diagnose(FILE_NAME):
    correlations = compute_correlations(FILE_NAME)
    
    most_positive = max(correlations, key=correlations.get)
    most_negative = min(correlations, key=correlations.get)

    return most_positive, most_negative
if __name__ == "__main__":
    reason_positive, reason_negative = diagnose(FILE_NAME)
    print(f"The most positively correlated event with becoming a squirrel is: {reason_positive}")
    print(f"The most negatively correlated event with becoming a squirrel is: {reason_negative}")
    print(f"Scott should avoid {reason_positive} and keep up {reason_negative}")