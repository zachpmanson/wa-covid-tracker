import jinja2
import os

def generate_index():
    os.system("sqlite3 wa_covid_data.db -html -header \"SELECT * FROM daily_cases\" > site/table.html")

    with open("site/table.html") as f:
        table = f.read()

    outputfile = "./site/index.html"
    subs = jinja2.Environment( 
                loader=jinja2.FileSystemLoader('./site/')      
                ).get_template('template.html').render(table=table) 

    with open(outputfile,'w') as f:
        f.write(subs)