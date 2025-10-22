"""Tests for the encounters module."""

import pytest
import immigration_enforcement.borderpatrol.encounters as encounters
from datetime import datetime
import pandas as pd
from plotly.graph_objs import Figure


@pytest.mark.parametrize(
    "input_date, expected_date",
    [
        (datetime(2025, 1, 1), datetime(2025, 1, 1)),
        (datetime(2025, 2, 1), datetime(2025, 2, 1)),
        (datetime(2025, 3, 1), datetime(2025, 3, 1)),
        (datetime(2025, 4, 1), datetime(2025, 4, 1)),
        (datetime(2025, 5, 1), datetime(2025, 5, 1)),
        (datetime(2025, 6, 1), datetime(2025, 6, 1)),
        (datetime(2025, 7, 1), datetime(2025, 7, 1)),
        (datetime(2025, 8, 1), datetime(2025, 8, 1)),
        (datetime(2025, 9, 1), datetime(2025, 9, 1)),
        (datetime(2025, 10, 1), datetime(2024, 10, 1)),
        (datetime(2025, 11, 1), datetime(2024, 11, 1)),
        (datetime(2025, 12, 1), datetime(2024, 12, 1)),
    ],
)
def test_convert_fiscal_date_to_calendar_date(input_date, expected_date):
    """
    The fiscal year starts October 1. So October 1, 2000 is part of Fiscal Year 2001.
    Test that the subtraction is only applied to three months: October, November, and December.
    """
    assert encounters._convert_fiscal_date_to_calendar_date(input_date) == expected_date


def _test_encounters_df_structure(df):
    """
    There are two "encounter" datasets which are merged to form the final one in the app:
        1. One of historic data
        2. One of Fiscal Year-to-Date data
    This test tests elements common to both structures
    """
    # It's a df type, has certain columns, and the columns are of certain types
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["date", "encounters"]
    assert pd.api.types.is_datetime64_ns_dtype(df["date"])
    assert pd.api.types.is_integer_dtype(df["encounters"])

    # Cadence of dates are monthly, with no missing or duplicate months
    expected_dates = pd.Series(
        pd.date_range(start=df["date"].min(), end=df["date"].max(), freq="MS")
    )
    actual_dates = pd.Series(df["date"].unique()).sort_values().reset_index(drop=True)
    assert actual_dates.equals(expected_dates)

    assert df["date"].is_unique
    assert (df["encounters"] >= 0).all()


def test_get_historic_sw_border_encounters():
    df = encounters._get_historic_sw_border_encounters()

    _test_encounters_df_structure(df)

    # The historic dataset starts in October 1999 (the start of the fiscal year) and should end in
    # September (i.e. it should encompass the whole fiscal year).
    # Note that the dataset actually includes the first few months of the next year, but that overlaps with
    # YTD dataset, and so I remove it to remove duplicates.
    assert df["date"].min() == pd.Timestamp("1999-10-01")
    assert df["date"].max().month == 9


def test_get_ytd_sw_border_encounters():
    df = encounters._get_ytd_sw_border_encounters()

    _test_encounters_df_structure(df)

    assert df["date"].min().month == 10  # Starts at beginning of fiscal year
    assert len(df) <= 12  # Never more than 1 year of data


def test_get_sw_border_encounters():
    df = encounters.get_sw_border_encounters()

    _test_encounters_df_structure(df)


def test_get_sw_border_encounters_graph():
    fig = encounters.get_sw_border_encounters_graph()

    assert isinstance(fig, Figure)
    assert len(fig.data) == 1  # Simple time series of encounters
