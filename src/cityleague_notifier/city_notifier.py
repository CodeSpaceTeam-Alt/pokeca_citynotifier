"""notify_city_league
"""

import json
from os import path

from line_message.line_message import Line
from selenium_searcher.league_searcher import PlayerClubSearcher


class WebChecker():
    def __init__(self, driver):
        self.searcher = PlayerClubSearcher(driver)

    def entry_list(self, id, filter):
        filtered_city_list = []
        city_list = self.searcher.search_league_list(id)
        ret = True
        for city_league in city_list:
            for key, value in filter.items():
                if city_league[key] != value:
                    ret = False
                    break
            if ret is True:
                print("hit", city_league)
                filtered_city_list.append(city_league)
            ret = True
        return filtered_city_list


class CityLeagueManager():
    """
    CityLeague Management Class
    """
    def __init__(self, token, driver):
        self.messanger = Line(token=token)
        self.checker = WebChecker(driver)
        self.league_list = []
        self.old_result = []

    def load_result(self, fn):
        if path.exists(fn) is False:
            return False
        with open(fn, "r", encoding="utf-8") as f:
            self.old_result = json.load(f)
        return True

    def save_result(self, fn):
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(self.league_list, f, indent=2, ensure_ascii=False)
        return True

    def check_entry(self, id, filter):
        ret = False
        self.league_list = self.checker.entry_list(id, filter)
        for league in self.league_list:
            if league not in self.old_result:
                ret = True
        return ret

    def notify_message(self):
        """notify_message, function

        notify CityLeague new-entry by Line messanger
        Returns:
            True : if message sending is success.
            False : if message sending is failed.
        """
        for league in self.league_list:
            event_info = []
            if league not in self.old_result:
                for key, value in league.items():
                    event_info.append(key + "\t" + value)
            msg = "\n".join(event_info)
            if self.messanger.notify(msg) is False:
                return False
        return True
