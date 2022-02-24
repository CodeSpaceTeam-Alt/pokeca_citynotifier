"""notify_city_league
"""

import json
from os import path

from line_message.line_message import Line
from selenium_searcher.league_searcher import PlayerClubSearcher


class CityLeagueManager():
    """CityLeague Management Class

    * Get tournament list from searcher
    * Check tournament is update or not
    * Notify updated-tounament information by LINE
    """

    def __init__(self, token, driver):
        self.messanger = Line(token=token)
        self.searcher = PlayerClubSearcher(driver)
        self.league_dict = {}
        self.old_result = {}

    def load_result(self, fn):
        """ Load before tournament information

        old tournament information is stored in class attribute self.old_result

        Args:
            fn (str): json filename which stored old result.

        Examples:
            >>> load_result("old_result.json")

        Returns:
            False : file not found.
            True  : other
        """

        if path.exists(fn) is False:
            return False
        with open(fn, "r", encoding="utf-8") as f:
            self.old_result = json.load(f)
        return True

    def save_result(self, fn):
        """ Save latest tournament information

        Args:
            fn (str): json filename which store latest result.

        Examples:
            >>> save_result("old_result.json")

        Returns:
            True  : Any
        """
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(self.league_dict, f, indent=2, ensure_ascii=False)
        return True

    def check_entry(self, league_id, find_filter):
        """ Check new tournament entry exist

        Note:
            if you wish to compare old result, shall execute self.load_result before doing this function.

        Args:
            league_id (str): city_league id.
            find_filter (dict): filter your wish regulation

        Examples:
            if you check...

            - url : "https://event.pokemon-card.com/prior-reception-gym-events/XXXX"
            - enable to entry

            >>> check_entry("XXXX", {"ステータス": "エントリー"})
            True

        Returns:
            True  : new tournament is exist.
            False : new tournament is not exist.
        """
        ret = False
        self.league_dict = self.searcher.search_league_with_filter(league_id, find_filter)
        for tournament_id in self.league_dict:
            if tournament_id not in self.old_result:
                ret = True
        return ret

    def notify_message(self):
        """notify_message, function

        notify CityLeague new-entry by Line messanger
        Returns:
            True : if message sending is success.
            False : if message sending is failed.
        """
        for id_value, detail in self.league_dict.items():
            event_info = ["[受付中]" + self.searcher.league_title, self.searcher.url]
            if id_value not in self.old_result:
                for key, value in detail.items():
                    event_info.append(key + "\t" + value)
            msg = "\n".join(event_info)
            if self.messanger.notify(msg) is False:
                return False
        return True
