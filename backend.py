import borderpatrol.encounters as encounters
import detentions
from typing import Literal, Optional
from plotly.graph_objs import Figure
from type_defs import AuthorityType


def get_graph(
    dataset: Literal["Arresting Authority", "Criminality", "Border Patrol"],
    display: Optional[Literal["Count", "Percent"]],
    authority: AuthorityType,
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
