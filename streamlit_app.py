import streamlit as st
import backend as be

st.title("US Immigration Detention Data")
st.write(
    "Data comes from TRAC Reports' "
    "[ICE Detainees](https://tracreports.org/immigration/detentionstats/pop_agen_table.html) page. "
    "'ICE' stands for Immigration and Customs Enforcement. "
    "'CBP' stands for Customs and Border Protection."
)

fig = be.get_detention_chart()
st.plotly_chart(fig, use_container_width=True)
st.write(
    "Below is the raw dataset which fuels the ICE Detentions page "
    "([link](https://tracreports.org/immigration/detentionstats/pop_agen_table.json))."
)

df = be.get_detention_data()
st.data_editor(df)
