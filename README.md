# WA COVID-19 Tracker

All this currently does is scrape the case numbers from articles on [this page](https://ww2.health.wa.gov.au/News/Media-releases-listing-page), save it in a sqlite database and produce visualisations of it.

To install python dependencies:
```bash
pip install -r requirements.txt
```

To scrape data and generate page:
```bash
python3 main.py [days_to_chart]
```

Running will search for new articles, scrape them for their data, store data in a sqlite database, generate plots, and then create an HTML file to display it.

First run will download scrape all articles since 2021-01-01 and create a sqlite database to store that data in (>400 HTTP requests).  It will also (re)generate `site/index.html` based on `site/template.html` and `site/table.html`, and include the data visualisations.
