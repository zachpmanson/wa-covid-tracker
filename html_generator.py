import jinja2
import os
from datetime import datetime, timezone, timedelta

def generate_index(records):

    table_headings = ("Date", "Local Cases Overnight")

    # Get and convert time to AWST (UTC+8)
    now_utc = datetime.now()
    local_tz = timezone(timedelta(hours=8))
    current_time_awst = now_utc.astimezone(local_tz).strftime("%Y-%m-%d %H:%M:%S") + " AWST (UTC+8)"

    image_src = "./images/local_cases.png"

    outputfile = "./site/index.html"
    subs = jinja2.Environment( 
                loader=jinja2.FileSystemLoader('./site/')      
                ).get_template('template.html').render(
                    update_time=current_time_awst,
                    image_src=image_src,
                    table_headings=table_headings,
                    table_records=reversed(records)
                    ) 

    with open(outputfile,'w', encoding="utf-8") as f:
        f.write(subs)
