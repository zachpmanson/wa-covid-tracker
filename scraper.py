# scraper

import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np

def get_articles_since(earliest_date = dt.datetime.strptime("2020-12-31", "%Y-%m-%d").date()):
    """
    Gets all covid updates since specified date.
    By default retrieves all newer than 2020-12-31.  Returns a list of links.
    """
    r = requests.get("https://ww2.health.wa.gov.au/News/Media-releases-listing-page")
    soup = BeautifulSoup(r.content, "html.parser")
    accordian = soup.find("div", class_="threeCol-accordian")
    articles = accordian.find_all("li")
    covid_update_urls = []


    for li in articles:
        article_link = li.a
        print(f"{article_link.text=}")
        #if ("COVID-19 update" in article_link.text):
        # accounts for: hyphens, em dashes
        
        match_text = "COVID.?19( )+(U|u)pdate(.?){0,6}[0-9]+(st|nd|rd|th)?( )+[a-zA-Z]+( )+[0-9]{4}"
        if re.fullmatch(match_text, article_link.text.strip()):
            print(f"Is covid update:\n\t{article_link.text}")

            # COVID UPDATE must contain date.  Some have other headlines.
            date_obj = re.search("[0-9]+(st|nd|rd|th)?( )+[a-zA-Z]+( )+[0-9]{4}", article_link.text)
            if date_obj is not None:
                
                # remove date ordinals
                unclean_date = date_obj.group().split()
                clean_day = unclean_date[0].replace("st","").replace("nd","").replace("rd","").replace("th","")
                clean_date = " ".join([clean_day] + unclean_date[1:])

                date = dt.datetime.strptime(clean_date, "%d %B %Y").date()
                # Wish I could use Python 3.8+ f-strings but alas
                print(f"\t(date <= earliest_date)={(date <= earliest_date)}")
                if date <= earliest_date:
                    break
                covid_update_urls.append(article_link["href"])
        
        else:
            print(f"Not covid update:\n\t{article_link.text}")

    return covid_update_urls


def get_all_article_text(content_area):
    '''
    Extracts all text <p> from article.
    Converts written numbers 0-10 to digits.
    Returns concatenated string of all text within given content area.
    '''
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
    '''
    Gets the number of local cases from a given string.  Expects all numbers to
    be written as digits.
    '''
    # Is stored as set in case they really change it up and multiple options are needed
    formats = (
        "(([0-9]|,)+)( are)?( new)? local( COVID-19)?( cases)?",
    )

    local_cases_line_obj = re.search(formats[0],all_text)
    local_cases = None # defaults to 0 cases (should change to NaN or None)
    if local_cases_line_obj is not None:
        local_cases_line_text = local_cases_line_obj.group().replace(",","")
        local_cases_count_obj = re.search( "\d+", local_cases_line_text )
        local_cases = int( str( local_cases_count_obj.group() ) )
        
    print(f"{local_cases=}")
    return local_cases

def get_all_cases(all_text):
    '''
    Gets the number of cases from a given string.  Expects all numbers to
    be written as digits.
    '''
    # Is stored as set in case they really change it up and multiple options are needed
    formats = (
        "(total )?(of )?(([0-9]|,)+) new(?! local)( COVID-19)?( case(s?))?",
    )

    all_cases_line_obj = re.search(formats[0],all_text)
    all_cases = None # defaults to 0 cases (should change to NaN or None)
    if all_cases_line_obj is not None:
        all_cases_line_text = all_cases_line_obj.group().replace(",","")
        print(f"{all_cases_line_text=}\n{all_cases_line_obj.group()=}")
        all_cases_count_obj = re.search( "\d+", all_cases_line_text )
        all_cases = int( str( all_cases_count_obj.group() ) )
        
    print(f"{all_cases=}")
    return all_cases


def scrape_article(relative_url, data):
    url = "https://ww2.health.wa.gov.au/" + relative_url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    content_area = soup.find(id="contentArea")
    data["url"].append(url)
    data["dates"].append(get_date(content_area))

    all_text = get_all_article_text(content_area)
    
    data["local"].append(get_local_cases(all_text))
    data["all"].append(get_all_cases(all_text))
    #print(f"{data['local']}")
    #print(f"{data['all']}")