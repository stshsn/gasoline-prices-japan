from datetime import datetime, timezone

from bs4 import BeautifulSoup as bs
from requests import get as requests_get
from requests import head as requests_head
from requests.models import Response


class Scraper:
    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        self.excel_filename: str = ""

    def check_update(self, url: str, current_data: str) -> bool:
        res: Response = requests_head(self.base_url + url)
        last_modified: datetime = datetime.strptime(res.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

        current_datetime: datetime = datetime.fromisoformat(current_data)
        if last_modified > current_datetime:
            return True
        else:
            return False

    def get_newest_filename(self, url: str, current_datetime: datetime, user_agent: str) -> bool:
        headers = {"User-Agent": user_agent}
        with requests_get(self.base_url + url, stream=True, headers=headers) as res:
            print(f"GET {self.base_url + url} {res.status_code}")
            last_modified: datetime = datetime.strptime(res.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")
            if last_modified.tzinfo is None:
                last_modified = last_modified.replace(tzinfo=timezone.utc)
            print(f"LAST:{last_modified}, CURRENT:{current_datetime}")
            if last_modified > current_datetime:
                excel_filename: str = self.__get_excel_filename(res.content)
                self.excel_filename = excel_filename
                return True
            else:
                return False

    def get_excel_url(self) -> str:
        return self.base_url + self.excel_filename

    def __get_excel_filename(self, raw_html: bytes) -> str:
        raw_data = bs(raw_html, "lxml")
        main_div = raw_data.find(id="main")
        result_ul = main_div.find("ul", class_="ulist2")
        result_detail = result_ul.find_all("li")[1]
        result_excel_anchor = result_detail.find("a")
        excel_href_parts: list = result_excel_anchor["href"].split('/')[-1:]
        excel_filename: str = '/'.join(excel_href_parts)
        return excel_filename
