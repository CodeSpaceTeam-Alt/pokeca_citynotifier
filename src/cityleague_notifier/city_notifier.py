"""notify_city_league
"""

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

    def check_entry(self, id, filter):
        self.league_list = self.checker.entry_list(id, filter)
        ret = False
        if len(self.league_list) != 0:
            ret = True
        return ret

    def notify_message(self):
        """notify_message, function

        notify CityLeague new-entry by Line messanger
        Returns:
            True : if message sending is success.
            False : if message sending is failed.
        """
        msg_list = []
        for league in self.league_list:
            event_info = []
            for key, value in league.items():
                event_info.append(key + "\t" + value)
            msg_list.append("\n".join(event_info))
        
        msg = "\n====\n".join(msg_list)
        ret = self.messanger.notify(msg)
        return ret
