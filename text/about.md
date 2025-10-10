In 2025, President Trump increased immigration enforcement in the United States. That made me wonder: what was the baseline for immigration enforcement, and how much was it actually increasing? This app is my attempt to answer those questions—by visualizing publicly available data in a way that's accessible and up-to-date.

The app currently includes two datasets:

- **ICE Detentions**: Sourced from the Transactional Records Access Clearinghouse (TRAC), this dataset provides periodic snapshots of detainee populations held in ICE facilities. The data is scraped from TRAC’s [website](https://tracreports.org/immigration/detentionstats/pop_agen_table.html) and cached for 15 minutes. TRAC typically updates the data a few times per month.

- **Border Patrol Encounters**: Combines year-to-date data from [Customs and Border Protection (CBP)](https://www.cbp.gov/document/stats/southwest-land-border-encounters) with historic data from the [Office of Homeland Security Statistics (OHSS)](https://ohss.dhs.gov/khsm/cbp-encounters). CBP releases new data monthly via downloadable spreadsheets, which I manually download and process. The latest file used is *FY22–FY25 (FYTD) Southwest Land Border Encounters – August*.

To learn more about the data sources, methodology, and design choices, check out these blog posts:

- [A Python App for Analyzing Immigration Enforcement Data](https://arilamstein.com/blog/2025/07/21/a-python-app-for-analyzing-immigration-enforcement-data/)
- [Visualizing 25 Years of Border Patrol Data with Python](https://arilamstein.com/blog/2025/10/06/visualizing-25-years-border-patrol-data-python/)

This project is not affiliated with TRAC, CBP, or OHSS. Please direct any questions about the underlying data to those organizations.

The code for this app is [open source](https://github.com/arilamstein/immigration_enforcement). If you have questions, feedback, or want to collaborate on similar projects, feel free to reach out via [my website](https://arilamstein.com).
