from fastapi import FastAPI

from gasoline_prices.scraper import Scraper

app = FastAPI()

base_url: str = "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/"
scraper = Scraper(base_url)


@app.get("/")
def read_root():
    # ret = scraper.check_update("results.html", "2022-08-01")
    ret = scraper.get_newest_data("results.html", "2022-08-01")

    return {"ret": ret}
