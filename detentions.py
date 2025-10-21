"""
Functions to scrape and graph data from TRAC's "ICE Detainees" page
(https://tracreports.org/immigration/detentionstats/pop_agen_table.html).
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
from typing import cast, Sequence, Any, TypedDict
from datetime import datetime
from type_defs import AuthorityType

colorblind_palette = colorblind_palette = [
    "#377eb8",  # blue
    "#ff7f00",  # orange
    "#a65628",  # brown
    "#999999",  # gray
]


@st.cache_data(ttl="15m")
def get_detention_data() -> pd.DataFrame:
    """
    Get the data which powers TRAC's "ICE Detainees" page and return it as a dataframe.

    This function caches the data for 15 minutes. They seem to update the site just a few times a month, so this should
    be fine.

    URLS of interest:
    1. TRAC Reports homepage: https://tracreports.org/
    2. TRAC Reports Immigration page: https://tracreports.org/immigration/
    3. TRAC Reports Immigration Detention Quick Facts page:
       https://tracreports.org/immigration/quickfacts/detention.html
    4. The "See More Data" page when you get on "Detention Quick Facts":
       https://tracreports.org/immigration/detentionstats/pop_agen_table.html
    5. The JSON which populates the Detention Quick Facts page:
       https://tracreports.org/immigration/detentionstats/pop_agen_table.json

    This function gets the data from (5), does some light processing, and returns it.
    """
    response = requests.get(
        "https://tracreports.org/immigration/detentionstats/pop_agen_table.json"
    )

    df = pd.DataFrame(response.json())
    df.date = pd.to_datetime(df.date).dt.date

    return df


def get_aa_count_chart() -> Figure:
    """Get a chart that shows detentions by arresting authority as a count."""
    df = get_detention_data()

    df = df.rename(columns={"ice_all": "ICE", "cbp_all": "CBP", "total_all": "Total"})

    # Converts df from wide to long
    df_melted = df.melt(
        id_vars="date",
        value_vars=["ICE", "CBP", "Total"],
        var_name="Arresting Authority",
        value_name="count",
    )

    fig = px.line(
        df_melted,
        x="date",
        y="count",
        color="Arresting Authority",
        color_discrete_sequence=colorblind_palette,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Detainees",
        title="ICE Detainees by Date* and Arresting Authority",
    )

    return _style_detentions_graph(fig)


def get_aa_pct_chart() -> Figure:
    """Get a chart that shows detentions by arresting authority as a percent."""
    df = get_detention_data()

    df["ICE"] = (df.ice_all / df.total_all * 100).round()  # Rounding is in the original
    df["CBP"] = (df.cbp_all / df.total_all * 100).round()

    # Converts df from wide to long
    df_melted = df.melt(
        id_vars="date",
        value_vars=["ICE", "CBP"],
        var_name="Arresting Authority",
        value_name="percent",
    )

    fig = px.line(
        df_melted,
        x="date",
        y="percent",
        color="Arresting Authority",
        color_discrete_sequence=colorblind_palette,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Percent",
        title="ICE Detainees by Date* and Arresting Authority",
    )

    return _style_detentions_graph(fig)


def get_col_prefix(authority: AuthorityType) -> str:
    """
    Return the column prefix for the UI text "ICE", "CBP" and "All".

    When viewing the criminality dataset the UI lets users select stats for each arresting authority ("ICE", "CBP") and
    together ("All"). In the dataset, these subsets are denoted by the column prefixes "ice", "cbp" and "total". This
    function converts the UI text to the column prefix.
    """
    if authority == "All":
        return "total"
    elif authority == "ICE":
        return "ice"
    elif authority == "CBP":
        return "cbp"
    else:
        raise ValueError(f"Unknown authority {authority}")


def get_criminality_chart_title(authority: AuthorityType) -> str:
    """
    The chart title should specify whether the graph is of all detainees,
    or just those detainees who were arrested by a particular arresting authority.
    """
    if authority == "All":
        return "ICE Detainees by Date* and Criminality**"
    else:
        return f"ICE Detainees (Detained by {authority}) by Date* and Criminality**"


def get_criminality_count_chart(authority: AuthorityType) -> Figure:
    """Get a chart that shows the criminality of detainees by arresting authority as a count."""
    df = get_detention_data()

    # Converts df from wide to long
    prefix = get_col_prefix(authority)
    df = df.rename(
        columns={
            f"{prefix}_all": "Total",
            f"{prefix}_conv": "Convicted Criminal",
            f"{prefix}_pend": "Pending Criminal Charges",
            f"{prefix}_other": "Other Immigration Violator",
        }
    )

    df_melted = df.melt(
        id_vars="date",
        value_vars=[
            "Convicted Criminal",
            "Pending Criminal Charges",
            "Other Immigration Violator",
            "Total",
        ],
        var_name="Criminal Status",
        value_name="count",
    )

    fig = px.line(
        df_melted,
        x="date",
        y="count",
        color="Criminal Status",
        color_discrete_sequence=colorblind_palette,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Detainees",
        title=get_criminality_chart_title(authority),
    )

    return _style_detentions_graph(fig)


def get_criminality_pct_chart(authority: AuthorityType) -> Figure:
    """Get a chart that shows the criminality of detainees by arresting authority as a percent."""
    df = get_detention_data()

    prefix = get_col_prefix(authority)
    all_col = f"{prefix}_all"
    conv_col = f"{prefix}_conv"
    pend_col = f"{prefix}_pend"
    other_col = f"{prefix}_other"

    df["Convicted Criminal"] = (
        df[conv_col] / df[all_col] * 100
    ).round()  # Rounding is in the original
    df["Pending Criminal Charges"] = (df[pend_col] / df[all_col] * 100).round()
    df["Other Immigration Violator"] = (df[other_col] / df[all_col] * 100).round()

    # Converts df from wide to long
    df_melted = df.melt(
        id_vars="date",
        value_vars=[
            "Convicted Criminal",
            "Pending Criminal Charges",
            "Other Immigration Violator",
        ],
        var_name="Criminal Status",
        value_name="percent",
    )

    fig = px.line(
        df_melted,
        x="date",
        y="percent",
        color="Criminal Status",
        color_discrete_sequence=colorblind_palette,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Percent",
        title=get_criminality_chart_title(authority),
    )

    return _style_detentions_graph(fig)


def _get_max_y_value_from_figure(fig: Figure) -> float:
    values: list[float] = []
    for trace in fig.data:
        y = getattr(trace, "y", None)
        if y is None:
            continue
        seq = cast(
            Sequence[float], y
        )  # cast: plotly stubs type trace.y as Any; narrow to Sequence[float] for mypy
        values.extend(float(v) for v in seq if v is not None)

    return max(values) if values else 0.0


def _style_detentions_graph(fig: Figure) -> Figure:
    """
    Each graph in this module should have a similar style:
    1. A vertical line showing when presidential administrations changed.
    2. The legend should appear on the top. This is because some of the labels from TRAC are long and so
       the default placement (on the right, next to the lines) cuts significantly into the data portion of
       the graph. Especially on mobile, this makes the graph hard to read.
    """

    class Administration(TypedDict):
        President: str
        Start: datetime

    administrations: list[Administration] = [
        {"President": "Joe Biden", "Start": datetime(2021, 1, 20)},
        {"President": "Donald Trump", "Start": datetime(2025, 1, 20)},
    ]

    max_y = _get_max_y_value_from_figure(fig)

    for one_administration in administrations:
        fig.add_vline(
            x=cast(
                Any, one_administration["Start"]
            ),  # cast: plotly stub expects numbers but runtime accepts datetimes
            line_color="black",
            line_dash="dash",
        )
        fig.add_annotation(
            x=one_administration["Start"],
            y=max_y,
            text=one_administration["President"],
            xanchor="left",
            xshift=5,
            showarrow=False,
            yanchor="bottom",
        )

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(t=100),  # Increase top margin to prevent overlap
    )

    return fig
