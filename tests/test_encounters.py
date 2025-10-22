"""Tests for the encounters module."""

import pytest
import immigration_enforcement.borderpatrol.encounters as encounters
from datetime import datetime


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
