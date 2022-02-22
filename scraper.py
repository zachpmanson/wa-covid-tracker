# scraper

import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def get_articles_since(earliest_date = dt.datetime.strptime("2020-12-31", "%Y-%m-%d").date()):
    """
    Gets all covid updates since specified date.
    """
    r = requests.get("https://ww2.health.wa.gov.au/News/Media-releases-listing-page")
    soup = BeautifulSoup(r.content, "html.parser")
    accordian = soup.find("div", class_="threeCol-accordian")
    articles = accordian.find_all("li")
    covid_update_urls = []


    for li in articles:
        article_link = li.a
        if ("COVID-19 update" in article_link.text):
            print(f"Is covid update:")
            print(f"\t{article_link.text}")

            #print("\t"+article_link.text)
            date_obj = re.search("[0-9]+ [a-zA-Z]+ [0-9]{4}", article_link.text)
            if date_obj is not None:
                date = dt.datetime.strptime(date_obj.group(), "%d %B %Y").date()
                print(f"\t{(date <= earliest_date)=}")
                if date <= earliest_date:
                    break
                covid_update_urls.append(article_link["href"])
        
        else:
            print(f"Not covid update:")
            print(f"\t{article_link.text}")
    
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
