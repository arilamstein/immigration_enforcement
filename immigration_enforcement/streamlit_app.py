import streamlit as st
import immigration_enforcement.backend as be
import immigration_enforcement.text.footnotes as footnotes

st.title("How Has U.S. Immigration Enforcement Changed?")
st.markdown(
    """
    This app visualizes key datasets related to immigration enforcement in the United States.
    It was created to help people explore how enforcement levels have changed over time—
    especially in response to recent policy shifts. Use the tabs below to explore ICE detentions,
    Border Patrol encounters, and learn more about the project.
    """
)

ice_tab, border_tab, about_tab = st.tabs(
    ["🔒 ICE Detentions", "🛂 Border Patrol Encounters", "ℹ️ About"]
)
with ice_tab:
    st.markdown(
        """
        **ICE Detentions** shows periodic snapshots of detainee populations held in ICE facilities.
        You can explore how these numbers vary by arresting authority and criminality status. To learn more
        about this dataset, click
        [here](https://arilamstein.com/blog/2025/07/21/a-python-app-for-analyzing-immigration-enforcement-data/).
        """
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        dataset = st.selectbox("Dataset", ["Arresting Authority", "Criminality"])
    with col2:
        display = st.selectbox("Display", ["Count", "Percent"])
    with col3:
        # In the original dataset the "Criminality" table has 3 tables. This lets
        # you see how the criminality of detainees varies by arresting authority.
        authority: str | None
        if dataset == "Criminality":
            authority = st.selectbox("Arresting Authority", ["All", "ICE", "CBP"])
        else:
            authority = None

    fig = be.get_graph(dataset, display, authority)
    st.plotly_chart(fig, use_container_width=True)
    # Each dataset has different footnotes.
    st.markdown(footnotes.get_footnote(dataset), unsafe_allow_html=True)
with border_tab:
    st.markdown(
        """
        **Border Patrol Encounters** combines year-to-date data from CBP with historic data from OHSS.
        This view helps you explore long-term trends in border enforcement activity. To learn more about this
        dataset, click [here](https://arilamstein.com/blog/2025/10/06/visualizing-25-years-border-patrol-data-python/)
        and
        [here](https://arilamstein.com/blog/2025/10/16/visualizing-border-patrol-encounters-under-the-second-trump-administration/).
        """
    )
    fig = be.get_graph("Border Patrol", None, None)
    st.plotly_chart(fig, use_container_width=True)
with about_tab:
    st.write(open("text/about.md").read())
