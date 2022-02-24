import jinja2
import os
from datetime import datetime, timezone, timedelta

def generate_index():
    os.system("sqlite3 wa_covid_data.db -html -header \"SELECT * FROM daily_cases ORDER BY date DESC\" > site/table.html")

    with open("site/table.html") as f:
        table = f.read()

    now_utc = datetime.now()
    local_tz = timezone(timedelta(hours=8))
    current_time_awst = now_utc.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S") + " AWST (UTC+8)"

    outputfile = "./site/index.html"
    subs = jinja2.Environment( 
                loader=jinja2.FileSystemLoader('./site/')      
                ).get_template('template.html').render(table=table, update_time=current_time_awst) 

    with open(outputfile,'w', encoding="utf-8") as f:
        f.write(subs)
