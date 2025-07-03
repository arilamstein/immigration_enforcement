import streamlit as st
import requests
import pandas as pd
import plotly.express as px


@st.cache_data(ttl="1d")
def get_detention_data():
    """URLS of interest:
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


def get_aa_count_chart():
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
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig.update_layout(xaxis_title="Date", yaxis_title="Detainees")

    return fig


def get_aa_pct_chart():
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
        color_discrete_sequence=px.colors.qualitative.Safe,
    )

    fig.update_layout(xaxis_title="Date", yaxis_title="Percent")

    return fig
