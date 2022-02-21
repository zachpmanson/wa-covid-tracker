import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_local_cases(data):
    plt.xticks(rotation="vertical", fontsize="xx-small")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))

    
    plt.title(f"Overnight Local Cases Over Past {len(data['dates'])} Days")
    plt.ylabel("Overnight Local Cases")
    plt.xlabel("Date")

    plt.ylim(-2,max(data["local"])*1.1)

    plt.plot(data["dates"],data["local"])
    #plt.axhline([0], color="red", dashes=(1,2))

    plt.rcParams['savefig.dpi'] = 300
    plt.tight_layout()

    plt.savefig("local_cases.png")
    
def generate_all_plots(data):
    generate_local_cases(data)