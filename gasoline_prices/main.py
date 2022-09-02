from fastapi import FastAPI

from gasoline_prices.scraper import Scraper

app = FastAPI()
scraper = Scraper()


@app.get("/")
def read_root():
    # ret = scraper.check_update(
    #    "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/results.html", "2022-08-01"
    # )
    ret = scraper.get_newest_data(
        "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/results.html", "2022-08-01"
    )
    return {"ret": ret}
