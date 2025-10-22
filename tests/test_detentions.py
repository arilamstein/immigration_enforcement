"""Tests for the detentions module."""

import pytest
import immigration_enforcement.detentions as detentions
from unittest.mock import patch
import pandas as pd
import datetime
from plotly.graph_objs import Figure


def test_get_detention_data():
    # Actual data taken from https://tracreports.org/immigration/detentionstats/pop_agen_table.json on 2025-10-21
    mock_json = [
        {
            "date": "09/21/2025",
            "ice_all": 46015,
            "cbp_all": 13747,
            "total_all": 59762,
            "ice_other": 16523,
            "cbp_other": 11223,
            "total_other": 27746,
            "ice_pend": 13767,
            "cbp_pend": 1242,
            "total_pend": 15009,
            "ice_conv": 15725,
            "cbp_conv": 1282,
            "total_conv": 17007,
        }
    ]

    # This is a unit test - so assume the API returns the actual data it returned today
    with patch("immigration_enforcement.detentions.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_json

        df = detentions.get_detention_data()

    expected_columns = set(mock_json[0].keys())
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == expected_columns
    assert df.date.dtype == object
    assert df.loc[0, "ice_all"] == 46015


@pytest.fixture
def mock_detention_df():
    return pd.DataFrame(
        [
            {
                "date": datetime.date(2025, 9, 21),
                "ice_all": 46015,
                "cbp_all": 13747,
                "total_all": 59762,
                "ice_other": 16523,
                "cbp_other": 11223,
                "total_other": 27746,
                "ice_pend": 13767,
                "cbp_pend": 1242,
                "total_pend": 15009,
                "ice_conv": 15725,
                "cbp_conv": 1282,
                "total_conv": 17007,
            },
            {
                "date": datetime.date(2025, 9, 7),
                "ice_all": 44844,
                "cbp_all": 13922,
                "total_all": 58766,
                "ice_other": 15502,
                "cbp_other": 11228,
                "total_other": 26730,
                "ice_pend": 13546,
                "cbp_pend": 1313,
                "total_pend": 14859,
                "ice_conv": 15796,
                "cbp_conv": 1381,
                "total_conv": 17177,
            },
        ]
    )


def test_get_aa_count_chart_returns_expected_figure(mock_detention_df):
    with patch("immigration_enforcement.detentions.get_detention_data") as mock_get:
        mock_get.return_value = mock_detention_df

        fig = detentions.get_aa_count_chart()

    assert isinstance(fig, Figure)
    assert len(fig.data) == 3  # ICE, CBP and Total


def test_get_col_prefix_valid_inputs():
    """Test get_col_prefix with valid authority values."""
    assert detentions.get_col_prefix("All") == "total"
    assert detentions.get_col_prefix("ICE") == "ice"
    assert detentions.get_col_prefix("CBP") == "cbp"


def test_get_col_prefix_invalid_input():
    """Test get_col_prefix raises ValueError for invalid input."""
    with pytest.raises(ValueError) as e:
        detentions.get_col_prefix("FBI")
    assert "Unknown authority FBI" in str(e.value)
