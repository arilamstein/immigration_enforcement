In 2025 President Trump increased immigration enforcement in the
United States. This caused me to wonder what the baseline for immigration
enforcement was, and how much he was increasing it.

My first step was to find an authoritative dataset of immigration enforcement. 
The first few sites I visited had data in PDF documents and Excel workbooks,
both of which are hard to
work with using data science tools such as Python. I eventually found the
Transactional Records Access Clearinghouse (TRAC) website, which lists raw
data in HTML tables
([1](https://tracreports.org/immigration/quickfacts/), 
[2](https://tracreports.org/immigration/detentionstats/pop_agen_table.html)).
I had seen TRAC cited in newspapers, so I felt that it was trustworthy.

TRAC, however, does not provide a lot of options for visualizing the data. So I
decided to scrape the website and create
graphs of it myself. Since there are so many ways to slice and dice the data, I
decided to create a website to help me analyze it. This
website caches data for one hour, so it should never be significantly
out of date. 

TRAC was not involved in the creation of this website. Please direct any questions about the underlying data to TRAC.  

Please direct questions about this website
to me. You can contact me via my website, which is linked to below.