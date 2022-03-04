"""
official pokemon card HP searcher module
"""

from logging import getLogger

from selenium.webdriver.common.by import By

logger = getLogger(__name__)


class PlayerClubSearcher():
    """Official Pokemon-Card Players Club Web Scraper
    """
    def __init__(self, driver):
        self.driver = driver
        self.league_title = ""
        self.url = ""
        self.filtered_entry = {}

    def search_league(self, league_url=""):
        """Get All tournament list

        Args:
            league_url (str): city_league id.

        Examples:
            if you check...

            - url : "https://event.pokemon-card.com/prior-reception-gym-events/XXXX"

            >>> search_league("https://event.pokemon-card.com/prior-reception-gym-events/XXXX")
            {"12345":{"都道府県":"東京都",
                      "店舗":"カードショップ",
                      "日付":"2021/12/31",
                      "時間":"9:00",
                      "ステータス":"エントリー"},
             ....
            }

        Returns:
            dict: tournament dict
        """
        logger.info("search DB for %s", league_url)
        self.url = league_url
        self.driver.get(league_url)

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
            if len(elem_btn.text) != 0:
                league_dict.update({id_value: {
                                    "都道府県": elem_state.text,
                                    "店舗": elem_shop.text,
                                    "日付": elem_date.text,
                                    "時間": elem_time.text,
                                    "ステータス": elem_btn.text}})
        return league_dict

    def dump_tournament_info(self, league_dict):
        """get tournament list which can entry within filter

        Args:
            league_dict (dict): city league information dict get from search_league
        """
        for detail in league_dict.values():
            logger.debug("\n 都道府県:\t%s\n 店舗:\t%s\n 日付:\t%s\n 時間:\t%s\n ステータス:\t%s\n",
                         detail["都道府県"],
                         detail["店舗"],
                         detail["日付"],
                         detail["時間"],
                         detail["ステータス"]
                       )

    def search_league_with_filter(self, league_url, find_filter):
        """get tournament list which can entry within filter

        Args:
            league_url (str): city_league URL.
            find_filter (dict): filter your wish regulation

        Examples:
            if you check...

            - url : "https://event.pokemon-card.com/prior-reception-gym-events/XXXX"
            - enable to entry

            >>> search_league("https://event.pokemon-card.com/prior-reception-gym-events/XXXX", {"ステータス": "エントリー"})
            {"12345":{"都道府県":"東京都",
                      "店舗":"カードショップ",
                      "日付":"2021/12/31",
                      "時間":"9:00",
                      "ステータス":"エントリー"},
             ....
            }

        Returns:
            dict: filtered tournament dict
        """

        all_entry = self.search_league(league_url)
        self.dump_tournament_info(all_entry)
        ret = True
        for tournament_id, detail in all_entry.items():
            for key, value in find_filter.items():
                if detail[key] != value:
                    ret = False
                    break
            if ret is True:
                self.filtered_entry.update({tournament_id: detail})
            ret = True
        self.dump_tournament_info(self.filtered_entry)
        return self.filtered_entry

    def dump_league_list(self):
        """get city League list now holded

        Args:
            None

        Examples:
            >>> dump_league_list()
            1201    シティリーグ シーズン5 【シティリーグ シーズン5】
            1202    シティリーグ シーズン5 【シティリーグ シーズン5 ジュニア】

        Returns:
            bool: always return True
        """

        self.driver.get("https://event.pokemon-card.com/events/")
        elems_league_list = self.driver.find_elements(By.CLASS_NAME, "eventList__contents")
        for elem_league in elems_league_list:
            url = elem_league.get_attribute("href")
            elem_status = elem_league.find_element(By.CLASS_NAME, "eventList__entryWrapper").text
            elem_title = elem_league.find_element(By.CLASS_NAME, "eventList__infoAreaTitle").text
            if elem_status in ["エントリー受付中", "受付期間外"] and "シティリーグ" in elem_title:
                logger.info("\n status:\t%s\n name:\t%s\n url:\t%s\n=============", elem_status, elem_title, url)
        return True
