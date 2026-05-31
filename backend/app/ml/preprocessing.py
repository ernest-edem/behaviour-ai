import pandas as pd


def clean_dataset(df: pd.DataFrame):
    df = df.copy()

    df.fillna(0, inplace=True)

    return df