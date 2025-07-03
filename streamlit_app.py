import streamlit as st
import backend as be

st.title("US Immigration and Customs Enforcement (ICE) Detention Data")
st.write("Data comes from TRAC Reports' [ICE Detainees](https://tracreports.org/immigration/detentionstats/pop_agen_table.html) page.")

fig = be.get_detention_chart()
st.plotly_chart(fig, use_container_width=True)

df = be.get_detention_data()
st.data_editor(df)
