"""
Utility software for this Package
"""

from argparse import ArgumentParser
import sys
from os import path
import json
from logging import basicConfig, INFO, DEBUG, getLogger

from cityleague_notifier import VERSION
from cityleague_notifier.city_notifier import CityLeagueManager
from selenium_searcher.chrome import ChromeSeleniumWrapper


logger = getLogger(__name__)

def get_args():
    """
    get command-line arguments

    Returns:
        NameSpace: parser.parse_args()
    """
    parser = ArgumentParser(description='City League Notifier')
    parser.add_argument('-c', '--config', default="./config/pokeca_config.json")
    parser.add_argument('-v', '--verbose', action="store_true", help='debug log enable')

    subparsers = parser.add_subparsers()
    parser_notify = subparsers.add_parser('watch', help='see `watch -h`')
    parser_notify.add_argument('--token', type=str, default="", help='token')
    parser_notify.set_defaults(handler=watch_tournament)

    parser_version = subparsers.add_parser('version', help='show version')
    parser_version.set_defaults(handler=version)

    parser_eventlist = subparsers.add_parser('ev_list', help='show event list')
    parser_eventlist.set_defaults(handler=city_season_list)
    return parser


def version(args):
    """software version dump

    Args:
        args (namespace): argument parse result

    Note:
        This function is not used args.
        Because this argument is used other sub-command.
        this function has same arguments as the other cub-commands.
    Returns:
        bool: always True
    """
    logger.info("%s", VERSION)
    return True


def load_config(config_fn):
    """load config file

    Args:
        config_fn (str): config file path

    Returns:
        dict: config data in JSON format
    """
    if path.exists(config_fn) is not True:
        logger.error("config %s is not exist", config_fn)
        return {}
    with open(config_fn, "r", encoding="utf-8") as json_fp:
        user_config = json.load(json_fp)
    return user_config



def city_season_list(args):
    """dump city league list when held in now season.

    Args:
        args (namespace): argument parse result

    Returns:
        bool: always True
    """
    ret = False
    user_config = load_config(args.config)
    if len(user_config) == 0:
        return ret
    try:
        selenium_d = ChromeSeleniumWrapper("log", user_config["driver_fn"])
        manager = CityLeagueManager(token="", driver=selenium_d.driver)
        ret = manager.dump_eventlist()
    finally:
        selenium_d.close()
    return ret


def watch_tournament(args):
    """watch city league tournament

    Args:
        args (namespace): argument parse result

    Returns:
        bool: always True
    """
    ret = False
    user_config = load_config(args.config)
    if len(user_config) == 0:
        return ret
    try:
        selenium_d = ChromeSeleniumWrapper("log", user_config["driver_fn"])
        manager = CityLeagueManager(token=args.token, driver=selenium_d.driver)
        manager.load_result(user_config["log_fn"])
        if manager.check_entry(user_config["city_url"], user_config["tournament_filter"]) is True:
            ret = manager.notify_message()
        manager.save_result(user_config["log_fn"])
    finally:
        selenium_d.close()
    return ret


def main():
    """
    main function
    """

    parser = get_args()
    args = parser.parse_args()

    if args.verbose is True:
        basicConfig(level=DEBUG)
    else:
        basicConfig(level=INFO)

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    sys.exit(main())
