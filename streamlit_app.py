import streamlit as st
import backend as be
import text.footnotes as footnotes

st.title("Immigration Enforcement Explorer")

ice_tab, border_tab, about_tab = st.tabs(
    ["🔒 ICE Detentions", "🛂 Border Patrol Encounters", "ℹ️ About"]
)
with ice_tab:
    col1, col2, col3 = st.columns(3)
    with col1:
        dataset = st.selectbox("Dataset", ["Arresting Authority", "Criminality"])
    with col2:
        display = st.selectbox("Display", ["Count", "Percent"])
    with col3:
        # In the original dataset the "Criminality" table has 3 tables. This lets
        # you see how the criminality of detainees varies by arresting authority.
        if dataset == "Criminality":
            authority = st.selectbox("Arresting Authority", ["All", "ICE", "CBP"])
        else:
            authority = None

    fig = be.get_graph(dataset, display, authority)
    st.plotly_chart(fig, use_container_width=True)
    # Each dataset has different footnotes.
    st.markdown(footnotes.get_footnote(dataset), unsafe_allow_html=True)
with border_tab:
    fig = be.get_graph("Border Patrol", None, None)
    st.plotly_chart(fig, use_container_width=True)
with about_tab:
    st.write(open("text/about.md").read())

st.markdown(
    """
    ---
    :small[Created by [Ari Lamstein](https://arilamstein.com/).
    View the source code
    [here](https://github.com/arilamstein/immigration_enforcement).]
    """
)
