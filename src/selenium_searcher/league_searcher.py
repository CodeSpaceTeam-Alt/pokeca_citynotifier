"""
official pokemon card HP searcher module
"""

from logging import getLogger

from selenium.webdriver.common.by import By

logger = getLogger(__name__)


class PlayerClubSearcher():
    """Official Pokemon-Card Players Club Web Scraper
    """
    def __init__(self, driver, league_id=""):
        self.driver = driver
        self.baseurl = "https://event.pokemon-card.com/prior-reception-gym-events"
        self.league_id = league_id

    @property
    def url(self):
        return "/".join([self.baseurl, self.league_id])

    def search_league_list(self, league_id=""):
        if len(league_id) != 0:
            self.league_id = league_id
        logger.info("search DB for %s", self.url)

        self.driver.get(self.url)

        elems_league_list = self.driver.find_elements(By.CLASS_NAME, "eventDetailContents__leagueListBoxColumns")
        league_list = []
        for elem_league in elems_league_list:
            elem_state = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemPref")
            elem_shop = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemTwinBox")
            elem_time = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemTime")
            elem_btn = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemButton")
            league_list.append({"state": elem_state.text, 
                                "shop": elem_shop.text, 
                                "time": elem_time.text, 
                                "status": elem_btn.text})
        return league_list
