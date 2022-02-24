"""Error Decorator modules"""

import selenium.common.exceptions as selenium_err


def general_err_deco(func):
    """general_err_deco
    """

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except FileNotFoundError:
            print("[Error] file not found")
            return False

        except KeyError as err:
            print("[Error] key not found", err.args[0])
            return False
        return True
    return wrapper


def selenium_err_deco(func):
    """selenium err decorator
    """

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except selenium_err.TimeoutException as err:
            print("[Error] timeout about ", err.args)
            return False
        return True
    return wrapper
