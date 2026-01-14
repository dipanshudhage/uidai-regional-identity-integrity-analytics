import pandas as pd

def load_data():
    enrol = pd.read_csv("data_enrolment.csv")
    demo  = pd.read_csv("data_demographic_updates.csv")
    bio   = pd.read_csv("data_biometric_updates.csv")

    return enrol, demo, bio
