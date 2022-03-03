import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
import numpy as np

def generate_cases(data, n_days, dark=False):
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    local_cases_array = np.array(data["local"][-n_days:], dtype=np.float)
    all_cases_array = np.array(data["all"][-n_days:], dtype=np.float)

    if dark:
        plt.style.use("./site/styles/dracula.mplstyle")

    plt.figure()

    plt.plot(data["dates"][-n_days:], all_cases_array, marker=".", label="Total Cases Overnight", alpha=1)
    plt.plot(data["dates"][-n_days:], local_cases_array, linestyle=":", marker="4", label="Local Cases Overnight", alpha=1)
    
    plt.xticks(rotation="vertical", fontsize="xx-small")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))

    
    plt.title(f"New Daily Cases Over Past {n_days} Days")
    plt.ylabel("Cases")
    plt.xlabel("Date")

    plt.legend()
    plt.tight_layout()

    folder = "./site/images"
    if dark: 
        filename = f"{folder}/cases_dark.png"
    else: 
        filename = f"{folder}/cases.png"
    
    plt.savefig(filename, dpi=300, transparent=True)

    print(f"Generated {filename} with {n_days} days.")


def generate_all_plots(data, n_days):
    generate_cases(data, n_days)    
    generate_cases(data, n_days, dark=True)    
