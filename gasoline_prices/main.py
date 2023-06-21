from datetime import datetime, timedelta

from fastapi import FastAPI
from sqlalchemy import func

from gasoline_prices.database import async_session, database
from gasoline_prices.models.prices import Price
from gasoline_prices.parser import Parser
from gasoline_prices.schemas.misc import Status
from gasoline_prices.scraper import Scraper

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


data_source_title: str = "石油製品価格調査 - 経済産業省 資源エネルギー庁"
data_source_base_url: str = "https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/"
data_source_html: str = "results.html"
scraper = Scraper(data_source_base_url)


@app.get("/gasoline/get/")
async def read_by_type_and_range(
    oil_type, start: datetime = datetime.now() - timedelta(days=40), end: datetime = datetime.now()
):
    ret = await Price.read_by_type_and_range(oil_type, start, end)
    return ret


"""
@app.get("/debug/")
async def get_all():
    ret = await Price.read_all()
    print(type(ret[0]))
    return ret
"""


@app.get("/gasoline/update")
async def update_data():
    # ret = scraper.check_update(data_source_html, "2022-08-01")
    latest_updated_at = await Price.get_latest_updated_at()
    print(latest_updated_at)
    if latest_updated_at is None:
        latest_updated_at = datetime.fromisoformat("1900-01-01")
    isUpdated = scraper.get_newest_filename(data_source_html, latest_updated_at)

    if isUpdated:
        excel_url = scraper.get_excel_url()
        parser = Parser(excel_url)
        parser.fetch_excel_file()
        prices_dict = parser.parse_excel_file()
        for oil_type in prices_dict.keys():
            if oil_type == "hi_octane":
                oil_type_id = 1
            elif oil_type == "regular":
                oil_type_id = 2
            price_history = prices_dict[oil_type]
            for price_data in price_history:
                price = Price(
                    oil_type_id=oil_type_id,
                    survey_date=price_data["survey_date"],
                    price=price_data["price"],
                    ref_price=price_data["ref_price"],
                )
                async with async_session() as session:
                    price_record = await Price.read_by_type_and_date(price, session)
                    if price_record:
                        price.updated_at = func.now()
                        await price_record.update(price, session)
                        await session.commit()
                    else:
                        await Price.create(price)
        return "New data found! Updated."
    else:
        return "Not modified."


@app.get("/gasoline/status", response_model=Status)
async def get_status():
    last_updated_at = await Price.get_latest_updated_at()
    return {
        "last_updated": last_updated_at,
        "data_source": {
            "title": data_source_title,
            "url": data_source_base_url + data_source_html,
        },
    }
