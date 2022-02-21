# scraper

import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def get_all_articles(num_days_to_get):
    r = requests.get("https://ww2.health.wa.gov.au/News/Media-releases-listing-page")
    soup = BeautifulSoup(r.content, "html.parser")
    accordian = soup.find("div", class_="threeCol-accordian")
    articles = accordian.find_all("li")
    covid_update_urls = []

    num_days_found = 0
    i = 0
    while (num_days_found < num_days_to_get):
        li = articles[i]
        i += 1
        article_link = li.a
        
        if ("COVID-19 update" in article_link.text):
            covid_update_urls.append(article_link["href"])
            num_days_found += 1
            print(f"Is covid update ({num_days_found}/{num_days_to_get}):")
        else:
            print(f"Link not covid update:")
        print(f"\t{article_link.text}")

    '''for li in articles[:80]:
        article_link = li.a
        
        if ("COVID-19 update" in article_link.text):
            print(f"Link is covid update:")
            covid_update_urls.append(article_link["href"])
        else:
            print(f"Link not covid update:")
        print(f"\t{article_link.text}")'''
    print(f"Found {len(covid_update_urls)} articles")
    return covid_update_urls

def get_all_article_text(content_area):
    all_p = content_area.div.findAll("p", recursive=True)
    all_text = ""
    for p in all_p:
        all_text += p.text+"\n"

        # Sometimes low numbers are written in words
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    for i in range(len(words)):
        all_text = all_text.replace(words[i], str(i))

    return all_text

def get_date(content_area):
    date_string = content_area.h3.text.strip()
    date = dt.datetime.strptime(date_string, "%d %B %Y").date()
    print(date)
    return date

def get_local_cases(all_text):
        
    formats = (
        "([0-9]+)( are)?( new)? local( COVID-19)?( cases)?",
    )

    local_cases_text = re.search(formats[0],all_text)
    local_cases = 0
    if local_cases_text is not None:
        local_cases_obj = re.search( "\d+", local_cases_text.group() )
        local_cases = int( str( local_cases_obj.group() ) )
        
    print(local_cases)
    return local_cases


def scrape_article(url, data):
    r = requests.get("https://ww2.health.wa.gov.au/" + url)
    soup = BeautifulSoup(r.content, "html.parser")
    content_area = soup.find(id="contentArea")
        
    data["dates"].append(get_date(content_area))

    all_text = get_all_article_text(content_area)
    
    data["local"].append(get_local_cases(all_text))

data = {
    "dates":[],
    "local":[]
}

def scrape_data(num_days_to_get):
    articles = get_all_articles(num_days_to_get)
    data = {
        "dates":[],
        "local":[]
    }
    for article in articles:
        scrape_article(article, data)
    data["dates"].reverse()
    data["local"].reverse()
    print(data)
    return data
