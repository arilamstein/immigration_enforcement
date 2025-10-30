import pytest

pytestmark = pytest.mark.nbval

NOTEBOOK_DIR = "notebooks"


def test_notebooks():
    pass  # nbval will discover and run notebooks automatically
