import pandas as pd
from datetime import datetime


def convert_fiscal_date_to_calendar_date(fiscal_date):
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


def get_monthly_region_df(output_format="long"):
    """
    Read in the "Monthly Region" sheet from the "CBP Encounters" Spreadsheet.

    Note that the dataset lists dates using Fiscal Years, and those must be converted to Calendar Years
    to work properly with standard charting functions and other datasets.
    """

    valid_options = ("long", "wide")
    if output_format not in valid_options:
        raise ValueError(
            f"output_format must be one of {valid_options}. '{output_format}' given."
        )

    # Read in data
    df = pd.read_excel(
        "KHSM Encounters (USBP) fy25m11.xlsx", sheet_name="Monthly Region"
    )

    # Rename columns
    df = df.rename(columns={"Fiscal\nYear": "Fiscal_Year"})
    df.columns = df.columns.str.lower()

    # Create a FiscalDate column that is a datetime object that is a combination of the FiscalYear and Month columns.
    df.month = df.month.str.split().str[1]  # Convert "01 October" to just "October"
    df["fiscal_date"] = df.fiscal_year.astype(str) + " " + df.month
    df.fiscal_date = pd.to_datetime(df.fiscal_date, format="%Y %B")  # Day defaults to 1

    # Convert Fiscal Year to Calendar Year
    df["date"] = df.fiscal_date.apply(convert_fiscal_date_to_calendar_date)

    # Now subset columns
    df = df[["date", "region", "quantity"]]

    if output_format == "long":
        return df
    else:
        df = df.pivot(columns="region", index="date", values="quantity").reset_index()
        df.columns.name = None
        return df
