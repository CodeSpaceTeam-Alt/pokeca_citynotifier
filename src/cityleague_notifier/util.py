"""
Utility software for this Package
"""

from argparse import ArgumentParser
import sys
from os import path
import json

from cityleague_notifier import VERSION
from cityleague_notifier.city_notifier import CityLeagueManager
from selenium_searcher.chrome import ChromeSeleniumWrapper


def get_args():
    """
    get command-line arguments  

    Returns:
        NameSpace: parser.parse_args()
    """
    parser = ArgumentParser(description='City League Notifier')
    parser.add_argument('--token', type=str, default="", help='token')
    parser.add_argument('-v', '--version', action="store_true", help='show version')
    parser.add_argument('-c', '--config', default="./config/pokeca_config.json")
    return parser


def main():
    """
    main function

    Args:
        token (str) : LINE Secret-Token value
        config (str) : config file path
        version (bool, optional) : Flag to show Version
    """

    args = get_args()
    opt = args.parse_args()
    if opt.version is True:
        print(VERSION)
        return True
    if path.exists(opt.config) is not True:
        return False
    with open(opt.config, "r", encoding="utf-8") as json_fp:
        user_config = json.load(json_fp)

    ret = False
    try:
        selenium_d = ChromeSeleniumWrapper("log", user_config["driver_fn"])
        manager = CityLeagueManager(token=opt.token, driver=selenium_d.driver)
        manager.load_result(user_config["log_fn"])
        if manager.check_entry("1201", {"ステータス": "エントリー"}) is True:
            ret = manager.notify_message()
        manager.save_result(user_config["log_fn"])
    finally:
        selenium_d.close()
    return ret


if __name__ == "__main__":
    sys.exit(main())
