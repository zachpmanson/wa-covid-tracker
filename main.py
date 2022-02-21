import scraper
import plot_generator
import sqlite3

def scrape_days(days):
    data = scraper.scrape_data(days)
    return data

def generate_all_plots(data):
    plot_generator.generate_all_plots(data)

def store_data(data):
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
    connection = sqlite3.connect(
        "wa_covid_data.db",
        detect_types=sqlite3.PARSE_DECLTYPES |
        sqlite3.PARSE_COLNAMES
    )
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM daily_cases ORDER BY date")
    rows = cursor.fetchall()
    print(rows)
    # Reformat data for graphing
    data = {
        "dates":[],
        "local":[]
    }
    for row in rows:
        data["dates"].append(row[0])
        data["local"].append(row[1])
    
    return data


if __name__ == "__main__":
    #data = scrape_days(80)
    #store_data(data)
    data = (retrieve_stored_data())
    print("\n",data)
    generate_all_plots(data)