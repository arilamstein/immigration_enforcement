import streamlit as st
import backend as be

st.title("US Immigration Enforcement Data")
st.write(
    "Data comes from TRAC Reports' "
    "[ICE Detainees](https://tracreports.org/immigration/detentionstats/pop_agen_table.html) page. "
    "'ICE' stands for 'Immigration and Customs Enforcement'. "
    "'CBP' stands for 'Customs and Border Protection'."
)

col1, col2, col3 = st.columns(3)
with col1:
    dataset = st.selectbox("Dataset", ["Arresting Authority", "Criminality"])
with col2:
    display = st.selectbox("Display", ["Count", "Percent"])
with col3:
    # In the original dataset the "Criminality" table has 3 versions. This lets
    # you see whether the criminality of detainees varies by arresting authority.
    if dataset == "Criminality":
        authority = st.selectbox("Arresting Authority", ["All", "ICE", "CBP"])
    else:
        authority = None

fig = be.get_graph(dataset, display, authority)
st.plotly_chart(fig, use_container_width=True)

st.write(
    "Created by [Ari Lamstein](https://arilamstein.com/). "
    "View the source code [here](https://github.com/arilamstein/immigration_enforcement)."
)
