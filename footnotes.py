"""
These footnotes are taken verbatim from
https://tracreports.org/immigration/detentionstats/pop_agen_table.html.
We don't include the third and final footnote because it is not used anywhere
on the page.
"""


def get_abbreviations_text():
    return '"ICE" stands for "Immigration and Customs Enforcement". "CBP" stands for "Customs and Border Protection".'


def get_date_footnote_text():
    return (
        "*&nbsp;Dates before 11/15/2021 refer to the date ICE posted the data; "
        "dates after 11/15/2021 refer to the date the information was current as of."
    )


def get_criminality_footnote_text():
    return (
        "**&nbsp;ICE classifies an individual as a convicted criminal if they have been convicted "
        "of any criminal violation. Violations can range from serious felonies all the way down "
        "to a purely immigration violation (such as illegal entry which is a petty offense under "
        "the U.S. Code), or a violation which results in only in a fine such as not keeping a dog "
        "on a leash, fishing without a permit, driving a vehicle with a tail light out, etc. For "
        "historical series on ICE detainees identifying the most serious offense they have been "
        "convicted of along with other details such as when they entered the U.S., nationality, "
        "gender, etc. go to https://tracreports.org/phptools/immigration/detention/"
    )


def get_date_footnote():
    return f"""
        <p style='font-size: 0.85em; font-style: italic; margin-top: 10px;'>
        {get_abbreviations_text()}<br>
        {get_date_footnote_text()}
        </p>
        """


def get_criminality_footnote():
    return f"""
        <p style='font-size: 0.85em; font-style: italic; margin-top: 10px;'>
        {get_abbreviations_text()}<br>
        {get_date_footnote_text()}<br>
        {get_criminality_footnote_text()}
        </p>
        """


def get_footnote(dataset):
    if dataset == "Arresting Authority":
        return get_date_footnote()
    elif dataset == "Criminality":
        return get_criminality_footnote()
    else:
        raise ValueError(f"Unknown dataset {dataset}")
