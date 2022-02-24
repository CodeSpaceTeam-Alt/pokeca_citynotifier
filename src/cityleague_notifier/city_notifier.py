"""notify_city_league
"""

import json
from os import path

from line_message.line_message import Line
from selenium_searcher.league_searcher import PlayerClubSearcher


class WebChecker():
    def __init__(self, driver):
        self.searcher = PlayerClubSearcher(driver)
        self.all_entry = {}

    def entry_list(self, id, filter):
        filtered_entry = {}
        self.all_entry = self.searcher.search_league_dict(id)
        self.league_title = self.searcher.league_title
        self.url = self.searcher.url
        ret = True
        for id_value, detail in self.all_entry.items():
            for key, value in filter.items():
                if detail[key] != value:
                    ret = False
                    break
            if ret is True:
                print("hit", detail)
                filtered_entry.update({id_value: detail})
            ret = True
        self.filtered_entry = filtered_entry
        return filtered_entry


class CityLeagueManager():
    """
    CityLeague Management Class
    """
    def __init__(self, token, driver):
        self.messanger = Line(token=token)
        self.checker = WebChecker(driver)
        self.league_dict = {}
        self.old_result = {}

    def load_result(self, fn):
        if path.exists(fn) is False:
            return False
        with open(fn, "r", encoding="utf-8") as f:
            self.old_result = json.load(f)
        return True

    def save_result(self, fn):
        with open(fn, "w", encoding="utf-8") as f:
            json.dump(self.league_dict, f, indent=2, ensure_ascii=False)
        return True

    def check_entry(self, id, filter):
        ret = False
        self.league_dict = self.checker.entry_list(id, filter)
        for id_value in self.league_dict.keys():
            if id_value not in self.old_result:
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
            event_info = ["[受付中]" + self.checker.league_title, self.checker.url]
            if id_value not in self.old_result:
                for key, value in detail.items():
                    event_info.append(key + "\t" + value)
            msg = "\n".join(event_info)
            if self.messanger.notify(msg) is False:
                return False
        return True
