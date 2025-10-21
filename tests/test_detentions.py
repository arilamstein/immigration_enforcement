"""Tests for the detentions module."""

import pytest
from detentions import get_col_prefix


def test_get_col_prefix_valid_inputs():
    """Test get_col_prefix with valid authority values."""
    assert get_col_prefix("All") == "total"
    assert get_col_prefix("ICE") == "ice"
    assert get_col_prefix("CBP") == "cbp"


def test_get_col_prefix_invalid_input():
    """Test get_col_prefix raises ValueError for invalid input."""
    with pytest.raises(ValueError) as exc_info:
        get_col_prefix("FBI")
    assert "Unknown authority FBI" in str(exc_info.value)