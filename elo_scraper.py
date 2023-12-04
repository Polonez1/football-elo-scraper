from playwright.sync_api import Playwright, sync_playwright, expect


class EloParser:
    def __init__(self):
        self.url: str = "http://elofootball.com/"
        self.country_hrefs: dict = {}

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
                self.country_hrefs[country] = href

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(self.url)
            self.__collect_country_hrefs()


if "__main__" == __name__:
    elo = EloParser()
    elo.parse()
    print(elo.country_hrefs)

# powershell -ExecutionPolicy Bypass -File C:\iLegion\football_elo_scraper\venv\Scripts\Activate.ps1
