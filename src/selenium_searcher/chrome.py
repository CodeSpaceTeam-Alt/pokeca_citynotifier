"""
selenium wrapper for google-chrome
"""

from logging import getLogger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


logger = getLogger(__name__)


class ChromeSeleniumWrapper():
    """
    Selenium Controller by chromedriver

    Note :
        you shall get chromedriver.
        see: https://chromedriver.chromium.org/downloads
    """

    def __init__(self, save_dir, driver_fn):
        self.save_dir = save_dir
        self.outbound_day = 25
        self.inbound_day = 25

        options = ChromeOptions()
        options.add_argument('--headless')
        prefs = {"download.default_directory": self.save_dir + "/"}
        options.add_experimental_option("prefs", prefs)

        chrome_service = fs.Service(executable_path=driver_fn)
        self.driver = Chrome(service=chrome_service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.action_chains = ActionChains(self.driver)

    def close(self):
        """close selenium driver
        """
        self.driver.close()
        self.driver.quit()
