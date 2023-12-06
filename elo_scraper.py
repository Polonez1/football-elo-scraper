from playwright.sync_api import Playwright, sync_playwright, expect

import processing_data
import json
import pandas as pd


class EloParser:
    def __init__(self):
        self.url: str = "http://elofootball.com/"
        self.country_hrefs: dict = {}
        self.competition_data: dict = {}
        self.ranking_data: dict = {}
        self.matches_data: dict = {}

    def __get_season_string(self) -> str:
        season = (
            self.page.get_by_role("heading", name="Selected season:")
            .inner_text()
            .partition("Selected season:")[2]
            .strip()
        )
        return season

    def __append_data(
        self, df: pd.DataFrame, append_dict: dict, country: str, season: str
    ):
        json_data = df.to_json(orient="records", indent=1)
        json_data = json.loads(json_data)
        append_dict[country] = {}
        append_dict[country][season] = {}
        append_dict[country][season] = json_data

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
    def __get_table_by_nr(self, table_index: int) -> list:
        """find table by index and return table components

        Args:
            table_index (int): table place

        Returns:
            list: headers, rows
        """
        table_element = self.page.query_selector_all(".sortable.fixed.primary")
        table = table_element[table_index]
        table_data = table.evaluate(
            "(table) => { return { headers: Array.from(table.tHead.rows[0].cells, cell => cell.innerText.trim()), rows: Array.from(table.tBodies[0].rows, row => Array.from(row.cells, cell => cell.innerText.trim())) }; }"
        )
        headers = table_data.get("headers")
        rows = table_data.get("rows")

        return headers, rows

    def __collect_competition_data(self, season: str, country: str) -> None:
        headers, rows = self.__get_table_by_nr(table_index=0)
        df = processing_data.transform_competition_data(rows=rows, columns=headers)
        self.__append_data(
            df=df, append_dict=self.competition_data, season=season, country=country
        )

        with open("competition_data.json", "w", encoding="utf-8") as json_file:
            json.dump(elo.competition_data, json_file, ensure_ascii=False, indent=2)

    def __collect_raking_data(self, season: str, country: str) -> None:
        headers, rows = self.__get_table_by_nr(table_index=2)
        df = processing_data.transform_raking_data(columns=headers, rows=rows)
        self.__append_data(
            df=df, append_dict=self.ranking_data, season=season, country=country
        )

        with open("raking_data.json", "w", encoding="utf-8") as json_file:
            json.dump(elo.ranking_data, json_file, ensure_ascii=False, indent=2)

    def __collect_matches_data(self, season: str, country: str) -> None:
        headers, rows = self.__get_table_by_nr(table_index=4)
        data_dict = {"headers": headers, "rows": rows}
        df = processing_data.transform_matches_data(columns=headers, rows=rows)
        self.__append_data(
            df=df, append_dict=self.matches_data, season=season, country=country
        )

        with open("matches_data.json", "w", encoding="utf-8") as json_file:
            json.dump(elo.matches_data, json_file, ensure_ascii=False, indent=2)

    def __collect_elo_data(self, hrefs: dict):
        for i in hrefs.items():
            country = i[0]
            href = i[1]
            url = self.url + href
            self.page.goto(url, timeout=60000)
            season = self.__get_season_string()
            self.__collect_competition_data(season=season, country=country)
            self.__collect_raking_data(season=season, country=country)
            self.__collect_matches_data(season=season, country=country)

            # break

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(self.url, timeout=60000)
            self.__collect_country_hrefs()
            self.__collect_elo_data(hrefs=self.country_hrefs)


if "__main__" == __name__:
    elo = EloParser()
    elo.parse()


# powershell -ExecutionPolicy Bypass -File C:\iLegion\football_elo_scraper\venv\Scripts\Activate.ps1
# Set-ExecutionPolicy Bypass -Scope Process
# .\venv\Scripts\activate
