from datetime import datetime

from bs4 import BeautifulSoup as bs
from requests import get as requests_get
from requests import head as requests_head
from requests.models import Response


class Scraper:
    def check_update(self, url: str, current_data: str) -> bool:
        res: Response = requests_head(url)
        last_modified: datetime = datetime.strptime(res.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

        current_datetime: datetime = datetime.fromisoformat(current_data)
        if last_modified > current_datetime:
            return True
        else:
            return False

    def get_newest_data(self, url: str, current_data: str) -> tuple:
        current_datetime: datetime = datetime.fromisoformat(current_data)

        with requests_get(url, stream=True) as res:
            last_modified: datetime = datetime.strptime(res.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

            if last_modified > current_datetime:
                excel_filename: str = self.__get_excel_filename(res.content)
                return (True, excel_filename)
            else:
                return (False, "")

    def __get_excel_filename(self, raw_html: bytes) -> str:
        raw_data = bs(raw_html, "lxml")
        main_div = raw_data.find(id="main")
        result_dl = main_div.find("dl", class_="dlist_n")
        result_detail = result_dl.find_all("dd")[0]
        result_excel_anchor = result_detail.find("a", class_="excel")
        excel_filename: str = result_excel_anchor["href"]
        return excel_filename
