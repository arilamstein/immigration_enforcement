import immigration_enforcement.borderpatrol.encounters as encounters
import immigration_enforcement.detentions as detentions
from plotly.graph_objs import Figure


def get_graph(
    dataset: str,
    display: str | None,
    authority: str | None,
) -> Figure:
    """
    Get the graph specified by the dataset, display and authority.

    Parameters
    ----------
    - dataset: one of "Arresting Authority", "Criminality" or "Border Patrol"
    - display: one of "Count" or "Percent"
    - authority: one of "CBP" (for "Customers and Border Protection"), "ICE" (for "Immigration and Customers
    Enforcement") or "All" (for the total number)

    Returns
    -------
    - A plotly figure
    """
    if dataset == "Arresting Authority":
        if display == "Count":
            fig = detentions.get_aa_count_chart()
        elif display == "Percent":
            fig = detentions.get_aa_pct_chart()
    elif dataset == "Criminality":
        assert (
            authority is not None
        ), "Authority must be specified for Criminality dataset"
        if display == "Count":
            fig = detentions.get_criminality_count_chart(authority)
        elif display == "Percent":
            fig = detentions.get_criminality_pct_chart(authority)
    elif dataset == "Border Patrol":
        fig = encounters.get_sw_border_encounters_graph()

    if not fig:
        raise ValueError(
            f"Cannot create graph for dataset={dataset}, display={display}"
        )

    return fig
