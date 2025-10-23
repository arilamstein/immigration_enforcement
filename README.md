# immigration_enforcement
[![CI](https://github.com/arilamstein/immigration_enforcement/actions/workflows/lint.yml/badge.svg)](https://github.com/arilamstein/immigration_enforcement/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/arilamstein/immigration_enforcement/graph/badge.svg?token=2RYIEPNAR2)](https://codecov.io/gh/arilamstein/immigration_enforcement)

This [app](https://immigration-enforcement.streamlit.app/) visualizes key datasets related to immigration enforcement in the United States. It was created to help people understand how enforcement levels have changed over time—especially in response to recent policy shifts.

The app currently includes two datasets:

- **ICE Detentions**: Periodic snapshots of detainee populations held in ICE facilities, sourced from [TRAC Reports](https://tracreports.org/immigration/detentionstats/pop_agen_table.html).
- **Border Patrol Encounters**: Combines year-to-date data from [Customs and Border Protection (CBP)](https://www.cbp.gov/document/stats/southwest-land-border-encounters) with historic data from the [Office of Homeland Security Statistics (OHSS)](https://ohss.dhs.gov/khsm/cbp-encounters).

To learn more about the data sources and design choices, check out these blog posts:

- [A Python App for Analyzing Immigration Enforcement Data](https://arilamstein.com/blog/2025/07/21/a-python-app-for-analyzing-immigration-enforcement-data/)
- [Visualizing 25 Years of Border Patrol Data with Python](https://arilamstein.com/blog/2025/10/06/visualizing-25-years-border-patrol-data-python/)
- [Visualizing Border Patrol Encounters Under the Second Trump Administration](https://arilamstein.com/blog/2025/10/16/visualizing-border-patrol-encounters-under-the-second-trump-administration/)

If you'd like to run the app locally or modify it, please read [DEVELOPER.md](/DEVELOPER.md).

The code is open source. If you have questions, feedback, or want to collaborate on similar projects, feel free to contact me via my [website](https://arilamstein.com).
