import pandas as pd


def read_rules(file_path):

    df = pd.read_excel(file_path)

    df = df.fillna("")

    df.columns = df.columns.str.upper()

    return df.to_dict("records")