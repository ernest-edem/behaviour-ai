import pandas as pd
from typing import Any, Union


class DataCleaner:
    """Basic data cleaning utilities for raw assessment data."""

    @staticmethod
    def drop_unused_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Drop columns that are not needed for modelling."""
        return df.drop(columns=columns, errors='ignore')

    @staticmethod
    def fill_missing(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
        """Fill missing values according to the chosen strategy."""
        if strategy == "median":
            return df.fillna(df.median())
        if strategy == "zero":
            return df.fillna(0)
        return df.fillna(method="ffill")

    @staticmethod
    def clean(data: Any) -> Any:
        """
        Unified cleaning entry point used by the ML shadow pipeline.

        - If ``data`` is a DataFrame: apply drop_unused_columns + fill_missing.
        - Otherwise (Pydantic model, dict, etc.): return unchanged.
          The downstream FeatureBuilder handles value extraction.

        This method exists so that ``PredictionPipeline.run()`` can call
        ``self.cleaner.clean(data)`` without raising an AttributeError.
        """
        if isinstance(data, pd.DataFrame):
            df = DataCleaner.drop_unused_columns(data, columns=[])
            df = DataCleaner.fill_missing(df, strategy="median")
            return df

        # Non-DataFrame payload (Pydantic model / dict) — pass through.
        return data
