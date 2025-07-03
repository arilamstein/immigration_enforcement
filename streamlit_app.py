import streamlit as st
import backend as be

st.title("US Immigration Enforcement Data")
st.write(
    "Data comes from TRAC Reports' "
    "[ICE Detainees](https://tracreports.org/immigration/detentionstats/pop_agen_table.html) page. "
    "'ICE' stands for 'Immigration and Customs Enforcement'. "
    "'CBP' stands for 'Customs and Border Protection'."
)

aa_count_tab, aa_pct_tab = st.tabs(
    [
        "Detainees by Arresting Authority (Count)",
        "Detainees by Arresting Authority (Percent)",
    ]
)

with aa_count_tab:
    fig = be.get_aa_count_chart()
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "Below is the raw dataset which fuels the ICE Detentions page "
        "([link](https://tracreports.org/immigration/detentionstats/pop_agen_table.json))."
    )

with aa_pct_tab:
    fig = be.get_aa_pct_chart()
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "Below is the raw dataset which fuels the ICE Detentions page "
        "([link](https://tracreports.org/immigration/detentionstats/pop_agen_table.json))."
    )

df = be.get_detention_data()
st.data_editor(df)

st.write(
    "View the source code [here](https://github.com/arilamstein/immigration_enforcement). "
    "Created by [Ari Lamstein](https://arilamstein.com/)."
)
