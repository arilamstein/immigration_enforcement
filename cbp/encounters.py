"""
Functions to work with data on US Border Patrol "Encounters" with Removable Aliens.

The data is sourced from two official Department of Homeland Security (DHS) datasets:
  * CBP Encounters (https://ohss.dhs.gov/khsm/cbp-encounters): includes monthly data from October FY2000 through
    November FY2025. This module uses only data through FY2024 to avoid overlap with the FYTD dataset.
  * Southwest Land Border Encounters (https://www.cbp.gov/document/stats/southwest-land-border-encounters):
    includes fiscal year-to-date (FYTD) data from FY2022 through FY2025. This module uses only FY2025 (FYTD) data.

The above datasets were downloaded from the above websites and are stored in this directory.

Although Border Patrol encounters are reported across three regions - Southwest Land Border, Northern Land Border,
and Coastal Border - this module focuses exclusively on the Southwest Land Border.

The `encounters` module has two functions external users will want to call:
  * `get_sw_border_encounters`: returns a cleaned, merged, dataset of monthly encounters at the Southwest Land Border.
  * `get_sw_border_encounters_graph`: returns a preformatted graph of those encounters,
    suitable for display or analysis.
"""

import pandas as pd
from datetime import datetime
import plotly.express as px
from pathlib import Path


def _convert_fiscal_date_to_calendar_date(fiscal_date):
    """
    Convert a federal fiscal date to its corresponding calendar date.

    The U.S. federal fiscal year begins in October. For reporting purposes,
    dates in October through December are considered part of the following
    fiscal year. This function adjusts those dates by subtracting one year
    to align them with the calendar year.
    """
    if fiscal_date.month >= 10:
        return datetime(fiscal_date.year - 1, fiscal_date.month, fiscal_date.day)
    else:
        return fiscal_date


def _get_historic_sw_border_encounters():
    """
    Read in the "Monthly Region" sheet from the "USBP Encounters" Spreadsheet. The file comes from:
    https://ohss.dhs.gov/khsm/cbp-encounters ("CBP Encounters - USBP - November 2024")

    This dataset lists dates using Fiscal Years, and those must be converted to Calendar Years
    to work properly with Python.

    This dataset has data on encounters on all 3 borders (Coastal Land Border,
    Northern Land Border, Southwest Land Border). We subset to just Southwest Land Border.

    This dataset includes data on the first few months of the latest fiscal year. We subset to the last full fiscal
    year, as we later merge with another dataset that has year-to-date data on the latest fiscal year, and this avoids
    duplicates.
    """

    # Read in data
    # By using Path to construct the path, this function works if imported from a notebook in the same directory
    # or a module in another directory (ex. the streamlit app a directory above)
    module_dir = Path(__file__).parent
    file_path = module_dir / "KHSM Encounters (USBP) fy25m11.xlsx"
    df = pd.read_excel(file_path, sheet_name="Monthly Region")

    # Rename columns
    df = df.rename(columns={"Fiscal\nYear": "Fiscal_Year", "Quantity": "Encounters"})
    df.columns = df.columns.str.lower()

    # Create a FiscalDate column that is a datetime object that is a combination of the FiscalYear and Month columns.
    df.month = df.month.str.split().str[1]  # Convert "01 October" to just "October"
    df["fiscal_date"] = df.fiscal_year.astype(str) + " " + df.month
    df.fiscal_date = pd.to_datetime(df.fiscal_date, format="%Y %B")  # Day defaults to 1

    # Convert Fiscal Year to Calendar Year
    df["date"] = df.fiscal_date.apply(_convert_fiscal_date_to_calendar_date)

    # Subset by region
    region_mask = df["region"] == "Southwest Land Border"
    df = df[region_mask]

    # Subset to the last fiscal year.
    # We get that on the current fiscal year from another source, and want to avoid duplicates when we merge.
    LAST_FISCAL_YEAR = 2024
    last_fiscal_date = datetime(LAST_FISCAL_YEAR, 9, 30)
    fiscal_year_mask = df["date"] <= last_fiscal_date
    df = df[fiscal_year_mask]

    # Now subset columns
    df = df[["date", "encounters"]]

    return df


def _get_ytd_sw_border_encounters():
    """
    Data comes from https://www.cbp.gov/document/stats/southwest-land-border-encounters.
    File "FY22 - FY25 (FYTD) Southwest Land Border Encounters - August", which was the latest at the time of writing.

    Since the historical file we're using goes back to longer than this one, we just want the FYTD data from this file.

    The data has multiple rows for each month (they correspond to things like citizenship of encountered aliens).

    This dates here are listed as fiscal years, and must be converted to calendar dates.
    """
    # By using Path to construct the path, this function works if imported from a notebook in the same directory
    # or a module in another directory (ex. the streamlit app a directory above)
    module_dir = Path(__file__).parent
    file_path = module_dir / "sbo-encounters-fy22-fy25-aug.csv"
    df = pd.read_csv(file_path)

    # Subset to the latest year for Border Patrol
    mask = (df["Fiscal Year"] == "2025 (FYTD)") & (
        df["Component"] == "U.S. Border Patrol"
    )
    df = df[mask]

    # Extract just the year. Note that .str has two different meanings here:
    # string accessor (.split()) and also as a getter for elements in a list ([0]).
    # I.e. the "2025" from "2025 (FYTD)".
    df["Year"] = df["Fiscal Year"].str.split().str[0]

    # Now get the calendar date for each row
    df["fiscal_date"] = df["Year"] + " " + df["Month (abbv)"]
    df["fiscal_date"] = pd.to_datetime(
        df.fiscal_date, format="%Y %b"
    )  # Day defaults to 1
    df["date"] = df.fiscal_date.apply(_convert_fiscal_date_to_calendar_date)

    # There are multiple rows for each demographic (ex. citizenship). Sum for each date.
    df = df.groupby("date")["Encounter Count"].sum().reset_index()

    # Rename columns for consistency with historic dataset
    df = df.rename(columns={"Encounter Count": "encounters"})

    return df


def _assert_monthly_date_integrity(df):
    """
    Ensure that all dates in the df are unique, and that none are missing from start to end.
    """

    start = df["date"].min()
    end = df["date"].max()

    # Generate expected monthly dates (always first of month)
    expected_dates = pd.date_range(start=start, end=end, freq="MS")

    # Assert uniqueness and completeness
    actual_dates = pd.Series(df["date"].unique()).sort_values()

    assert len(actual_dates) == len(expected_dates), "Date count mismatch or duplicates"
    assert actual_dates.equals(
        pd.Series(expected_dates)
    ), "Dates are missing or misaligned"


def get_sw_border_encounters():
    """
    Get all available data on Southwest Border Encounters by US Border Patrol.

    This data is in two datasets: one historic, and one year-to-date. Merge them, and ensure no dates
    are missing or duplicate.
    """
    historic = _get_historic_sw_border_encounters()
    ytd = _get_ytd_sw_border_encounters()
    df = pd.concat([historic, ytd], ignore_index=True)

    _assert_monthly_date_integrity(df)

    return df


def get_sw_border_encounters_graph(annotate_administrations=True):
    df = get_sw_border_encounters()

    fig = px.line(
        df,
        x="date",
        y="encounters",
        title="Border Patrol Encounters at the Southwest Land Border",
        labels={"date": "Date", "encounters": "Encounters"},
    )

    if annotate_administrations:
        administrations = [
            # Include Clinton for reference, but comment out bc his administration did not start during the data period
            # {"President": "Bill Clinton", "Start": datetime(1993, 1, 20)},
            {"President": "George W. Bush", "Start": datetime(2001, 1, 20)},
            {"President": "Barack Obama", "Start": datetime(2009, 1, 20)},
            {"President": "Donald Trump", "Start": datetime(2017, 1, 20)},
            {"President": "Joe Biden", "Start": datetime(2021, 1, 20)},
            # Add a line for Trump's second term. But do not include a name, because there is not room for it
            # on the graph.
            {"President": "", "Start": datetime(2025, 1, 20)},
        ]

        # Add a vertical line on the date the administration started, and write the presdient's name on the top
        max_y = df["encounters"].max()

        for one_administration in administrations:
            fig.add_vline(
                x=one_administration["Start"], line_color="black", line_dash="dash"
            )
            fig.add_annotation(
                x=one_administration["Start"],
                y=max_y,
                text=one_administration["President"],
                xanchor="left",
                xshift=5,
                showarrow=False,
                yanchor="bottom",
            )

    return fig
