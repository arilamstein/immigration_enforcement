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

def get_detention_chart():
    df = get_detention_data()

    # Converts df from wide to long
    df_melted = df.melt(
        id_vars="date",
        value_vars=["ice_all", "cbp_all", "total_all"],
        var_name="category",
        value_name="count",
    )

    fig = px.line(
        df_melted,
        x="date",
        y="count",
        color="category",
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="ICE Detainee Counts Over Time",
    )

    return fig
