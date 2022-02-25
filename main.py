import scraper
import plot_generator
import html_generator
import sqlite3
import sys

def store_data(data):
    '''
    Stores given data in sqlite database called wa_covid_data.db.
    '''
    connection = sqlite3.connect(
        "wa_covid_data.db",
        detect_types=sqlite3.PARSE_DECLTYPES |
        sqlite3.PARSE_COLNAMES
    )
    cursor = connection.cursor()
    for i in range(len(data["dates"])):
        sql_command = (
        f"""INSERT INTO daily_cases(date, local_cases)
        VALUES ('{data['dates'][i].strftime('%Y-%m-%d')}', {data['local'][i]})
        ON CONFLICT (date) DO UPDATE SET local_cases={data['local'][i]};
        """
        )
        print(sql_command) 
        cursor.execute(sql_command)
    connection.commit()

def retrieve_stored_data():
    '''
    Extracts data from sqlite database called wa_covid_data.db.
    Returns dictionary with lists for each attribute of the table.
    If the database doesn't exist it will generate one with a single table.
    '''
    connection = sqlite3.connect(
        "wa_covid_data.db",
        detect_types=sqlite3.PARSE_DECLTYPES |
        sqlite3.PARSE_COLNAMES
    )
    cursor = connection.cursor()

    sql_command = (
    """CREATE TABLE IF NOT EXISTS daily_cases (
        date DATE PRIMARY KEY UNIQUE,
        local_cases INTEGER
    )""")
    print(sql_command)
    cursor.execute(sql_command)

    sql_command = "SELECT * FROM daily_cases ORDER BY date"
    print(sql_command)
    cursor.execute(sql_command)
    rows = cursor.fetchall()

    # Reformat data for graphing
    data = {
        "dates":[],
        "local":[]
    }
    for row in rows:
        data["dates"].append(row[0])
        data["local"].append(row[1])
    
    return data

def run_with_stored_data():
   
    data = retrieve_stored_data() # get prexisting data
    if len(data["dates"]) == 0:
        # Database was empty, get all articles since default limit
        articles = scraper.get_articles_since() 
    else:
        # get all articles newer than newest db record ()
        articles = scraper.get_articles_since(data["dates"][-1]) # get all articles newer than newest db record
        
    print(articles)

    for article in articles:
        scraper.scrape_article(article, data)

    store_data(data) # add all data to db, will update already existing records
    print(f"{len(data['dates'])} days stored")
    # Get new set from db. Calling again so data is sorted.  This is likely inefficient
    data = retrieve_stored_data()
    
    n_days = 80
    if len(sys.argv) == 2:
        n_days = int(sys.argv[1])

    plot_generator.generate_all_plots(data, n_days)

if __name__ == "__main__":
    run_with_stored_data()
    html_generator.generate_index()