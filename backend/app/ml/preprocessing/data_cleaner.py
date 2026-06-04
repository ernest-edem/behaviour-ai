import pandas as pd

class DataCleaner:
    """Basic data cleaning utilities for raw assessment data."""

    @staticmethod
    def drop_unused_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        return df.drop(columns=columns, errors='ignore')

    @staticmethod
    def fill_missing(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
        if strategy == "median":
            return df.fillna(df.median())
        if strategy == "zero":
            return df.fillna(0)
        return df.fillna(method="ffill")
