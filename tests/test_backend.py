import immigration_enforcement.backend as be
from plotly.graph_objects import Figure
import pytest


def test_get_graph_aa():
    fig = be.get_graph(dataset="Arresting Authority", display="Count", authority=None)
    assert isinstance(fig, Figure)

    fig = be.get_graph(dataset="Arresting Authority", display="Percent", authority=None)
    assert isinstance(fig, Figure)


def test_get_graph_criminality():
    fig = be.get_graph(dataset="Criminality", display="Count", authority="CBP")
    assert isinstance(fig, Figure)

    fig = be.get_graph(dataset="Criminality", display="Percent", authority="ICE")
    assert isinstance(fig, Figure)

    fig = be.get_graph(dataset="Criminality", display="Percent", authority="All")
    assert isinstance(fig, Figure)

    with pytest.raises(ValueError):
        be.get_graph(dataset="Criminality", display="Percent", authority=None)


def test_get_graph_bp():
    fig = be.get_graph(dataset="Border Patrol", display=None, authority=None)
    assert isinstance(fig, Figure)


def test_invalid_dataset():
    with pytest.raises(ValueError):
        be.get_graph(dataset="ooga booga", display="Percent", authority=None)
