import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def generate_local_cases(data, n_days, dark=False):
    plt.style.use("default")

    if dark:
        #plt.style.use("./site/styles/dracula.mplstyle")
        plt.style.use("dark_background")



    plt.xticks(rotation="vertical", fontsize="xx-small")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))

    
    plt.title(f"Overnight Local Cases Over Past {n_days} Days")
    plt.ylabel("Overnight Local Cases")
    plt.xlabel("Date")

    plt.ylim(-2,max(data["local"])*1.1)

    plt.plot(data["dates"][-n_days:],data["local"][-n_days:])

    #lt.rcParams['savefig.dpi'] = 300
    plt.tight_layout()

    folder = "./site/images"
    if dark: 
        filename = f"{folder}/local_cases_dark.png"
    else: 
        filename = f"{folder}/local_cases.png"
    
    plt.savefig(filename, dpi=300, transparent=True)#, facecolor="#282A36")

    print(f"Generated {filename} with {n_days} days.")

def generate_all_plots(data, n_days):
    generate_local_cases(data, n_days)    
    # apparently plt.styles.use() REQUIRES a literal. Don't know why
    generate_local_cases(data, n_days, dark=True)
