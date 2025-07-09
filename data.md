Data comes from the [ICE Detainees](https://tracreports.org/immigration/detentionstats/pop_agen_table.html) page from
the Transactional Records Access Clearinghouse (TRAC) website. I originally attempted to use official statistics, but
found those datasets hard to work with. Specifically, they were in PDF and Excel documents, which are difficult to
analyze using Python.

The dataset that powers the ICE Detainees page comes from
[this](https://tracreports.org/immigration/detentionstats/pop_agen_table.json) page in JSON format. This app reads that
dataset in as a dataframe, and then replicates the math which the ICE Detainees page does to generate each table on the
page. But whereas the ICE Detainees page outputs a table, this app generates a graph. 

You can see the math the ICE Detainees page does by viewing the source code for the page. If you'd like to check my
work, you can view the source code for the app [here](https://github.com/arilamstein/immigration_enforcement).

Below you can view the dataset as a dataframe, and also download it as a CSV file: