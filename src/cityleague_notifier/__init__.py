from logging import DEBUG, INFO, basicConfig


VERSION = "1.1.1"


def setup_logger(verbose=False):
    if verbose is False:
        log_format = '%(message)s'
        basicConfig(level=INFO, format=log_format)
    else:
        log_format = '%(levelname)-8s [%(asctime)s] %(funcName)s \t %(message)s'
        basicConfig(level=DEBUG, format=log_format)
