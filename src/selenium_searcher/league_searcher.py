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
        self.league_title = ""

    @property
    def url(self):
        """watching URL"""
        return "/".join([self.baseurl, self.league_id])

    def search_league(self, league_id=""):
        """Get All tournament list

        Args:
            league_id (str): city_league id.

        Examples:
            if you check "https://event.pokemon-card.com/prior-reception-gym-events/XXXX" enable to entry.
            >>> entry_list("XXXX")

        Returns:
            dict: tournament dict
        """

        if len(league_id) != 0:
            self.league_id = league_id
        logger.info("search DB for %s", self.url)

        self.driver.get(self.url)

        self.league_title = self.driver.find_element(By.CLASS_NAME, "eventDetailMainVisual__infoAreaTitle").text
        elems_league_list = self.driver.find_elements(By.CLASS_NAME, "eventDetailContents__leagueListBoxColumns")
        league_dict = {}
        for elem_league in elems_league_list:
            id_value = elem_league.get_attribute("id")
            elem_state = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemPref")
            elem_shop = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemHall")
            elem_date = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemDate")
            elem_time = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemTime")
            elem_btn = elem_league.find_element(By.CLASS_NAME, "eventDetailContents__leagueListBoxItemButton")
            league_dict.update({id_value: {
                                "都道府県": elem_state.text,
                                "店舗": elem_shop.text,
                                "日付": elem_date.text,
                                "時間": elem_time.text,
                                "ステータス": elem_btn.text}})
        return league_dict

    def search_league_with_filter(self, league_id, find_filter):
        """get tournament list which can entry within filter

        Args:
            league_id (str): city_league id.
            find_filter (dict): filter your wish regulation

        Examples:
            if you check "https://event.pokemon-card.com/prior-reception-gym-events/XXXX" enable to entry.
            >>> entry_list("XXXX", {"ステータス": "エントリー"})

        Returns:
            dict: filtered tournament dict
        """

        filtered_entry = {}
        all_entry = self.search_league(league_id)
        ret = True
        for tournament_id, detail in all_entry.items():
            for key, value in find_filter.items():
                if detail[key] != value:
                    ret = False
                    break
            if ret is True:
                filtered_entry.update({tournament_id: detail})
            ret = True
        return filtered_entry
