from playwright.sync_api import Playwright, sync_playwright, expect

import processing_data
import json


class EloParser:
    def __init__(self):
        self.url: str = "http://elofootball.com/"
        self.country_hrefs: dict = {}
        self.competition_data: dict = {"data": []}
        self.ranking_data: dict = {}
        self.matches_data: dict = {}

    def _season_hrefs_collector(self):
        pass

    def __collect_country_hrefs(self):
        dropdown_menus = self.page.query_selector_all(".dropdown-menu")
        country_hrefs_box = dropdown_menus[0]
        if country_hrefs_box:
            hrefs_element = country_hrefs_box.query_selector_all("a")
            for i in hrefs_element:
                country = i.inner_text()
                href = i.get_attribute("href")
                if country == "UEFA Competitions":
                    pass
                else:
                    self.country_hrefs[country] = href

    # ------------------------------------------------------------------------------------------------------#
    def __collect_competition_data(self):
        table_element = self.page.query_selector_all(".sortable.fixed.primary")
        table = table_element[0]
        table_data = table.evaluate(
            "(table) => { return { headers: Array.from(table.tHead.rows[0].cells, cell => cell.innerText.trim()), rows: Array.from(table.tBodies[0].rows, row => Array.from(row.cells, cell => cell.innerText.trim())) }; }"
        )
        headers = table_data.get("headers")
        rows = table_data.get("rows")
        data_dict = {"headers": headers, "rows": rows}
        json_data = json.dumps(data_dict, ensure_ascii=False, indent=2)

        self.competition_data["data"] = json_data

    def __collect_raking_data(self):
        pass

    def __collect_matches_data(self):
        pass

    def __collect_elo_data(self, hrefs: dict):
        for i in hrefs.items():
            country = i[0]
            href = i[1]
            url = self.url + href
            self.page.goto(url)
            self.__collect_competition_data()

            break

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(self.url)
            self.__collect_country_hrefs()
            self.__collect_elo_data(hrefs=self.country_hrefs)


if "__main__" == __name__:
    elo = EloParser()
    elo.parse()
    print(elo.competition_data)

# powershell -ExecutionPolicy Bypass -File C:\iLegion\football_elo_scraper\venv\Scripts\Activate.ps1
