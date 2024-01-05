from datetime import datetime
from io import BytesIO
from typing import BinaryIO

from requests import get as requests_get
from xlrd import open_workbook, xldate_as_tuple

HI_OCTANE_ROWS: range = range(9, 15)
REGULAR_ROWS: range = range(15, 21)
DATE_COL: int = 3  # "D"
PRICE_COL: int = 14  # "O"
REF_COL: int = 15  # "P"


class Parser:
    def __init__(self, excel_url: str, user_agent: str) -> None:
        self.excel_url: str = excel_url
        self.user_agent: str = user_agent

    def fetch_excel_file(self) -> bool:
        headers = {"User-Agent": self.user_agent}
        print(f"GET {self.excel_url}")
        excel_data: bytes = requests_get(self.excel_url, headers=headers).content
        self.excel_data: BinaryIO = BytesIO(excel_data)

        return True

    def parse_excel_file(self) -> dict:
        prices: dict = dict()
        prices["hi_octane"] = self.__create_prices_by_type("hi_octane", HI_OCTANE_ROWS)
        prices["regular"] = self.__create_prices_by_type("regular", REGULAR_ROWS)

        self.excel_data.close()
        return prices

    def __create_prices_by_type(self, oil_type, target_rows) -> list:
        self.excel_data.seek(0)
        wb = open_workbook(file_contents=self.excel_data.read())
        ws = wb.sheet_by_index(0)

        prices_by_type: list = list()
        for row in target_rows:
            survey_date = datetime(*xldate_as_tuple(ws.cell_value(rowx=row, colx=DATE_COL), wb.datemode)).date()
            price = ws.cell_value(rowx=row, colx=PRICE_COL)
            ref_price = ws.cell_value(rowx=row, colx=REF_COL)
            prices_by_type.append({"survey_date": survey_date, "price": price, "ref_price": ref_price})

        return prices_by_type
