from fastapi import FastAPI

from gasoline_prices.scraper import Scraper

app = FastAPI()

base_url: str = "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/"
scraper = Scraper(base_url)


@app.get("/")
def read_root():
    # ret = scraper.check_update("results.html", "2022-08-01")
    isUpdated = scraper.get_newest_filename("results.html", "2022-08-01")

    if isUpdated:
        return scraper.get_excel_url()
    else:
        return "Not modified."
