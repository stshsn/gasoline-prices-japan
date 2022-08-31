from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs


class Scraper:
    def check_update(self, url, current_data):
        res = requests.head(url)
        last_modified = datetime.strptime(res.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

        current_data = datetime.fromisoformat(current_data)
        if last_modified > current_data:
            return True
        else:
            return False

    def get_newest_data(self, url, current_data):
        current_data = datetime.fromisoformat(current_data)

        with requests.get(url, stream=True) as res:
            last_modified = datetime.strptime(res.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")

            if last_modified > current_data:
                excel_filename = self.__get_excel_filename(res.content)
                return (True, excel_filename)
            else:
                return (False, "")

    def __get_excel_filename(self, raw_html):
        raw_data = bs(raw_html, "lxml")
        main_div = raw_data.find(id="main")
        result_dl = main_div.find("dl", class_="dlist_n")
        result_detail = result_dl.find_all("dd")[0]
        result_excel_anchor = result_detail.find("a", class_="excel")
        excel_filename = result_excel_anchor["href"]
        return excel_filename
