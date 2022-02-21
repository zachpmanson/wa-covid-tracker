import scraper
import plot_generator

def run():
    data = scraper.scrape_data(80)
    plot_generator.generate_all_plots(data)

if __name__ == "__main__":
    run()