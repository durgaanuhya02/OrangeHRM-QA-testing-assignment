"""
BasePage centralises the Selenium wait/interaction logic shared by
every page object, so individual page classes only need to declare
locators and business-flow methods instead of repeating
WebDriverWait boilerplate everywhere.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from utils.config import DEFAULT_TIMEOUT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Explicit-wait helpers (no time.sleep anywhere in the framework)
    # ------------------------------------------------------------------
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def is_element_present(self, locator, timeout=None):
        """Returns True/False instead of raising -- used for negative
        assertions where the element is genuinely expected to be absent."""
        try:
            local_wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
            local_wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def click(self, locator):
        self.find_clickable(locator).click()

    def type_text(self, locator, text):
        """Clears the field and types `text`.

        Plain `.clear()` is not reliable on OrangeHRM's Vue-controlled
        inputs (e.g. the Employee Name autocomplete): it can empty the
        DOM value without updating Vue's internal state, so a
        following send_keys() ends up appended after the old value
        instead of replacing it. Selecting all text and deleting it
        via the keyboard mirrors what a real user would do and keeps
        the component's own state in sync.
        """
        field = self.find_visible(locator)
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(text)

    def get_text(self, locator):
        return self.find_visible(locator).text.strip()

    def hover(self, locator):
        element = self.find_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def wait_for_url_contains(self, fragment, timeout=None):
        local_wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
        return local_wait.until(EC.url_contains(fragment))

    def wait_until_stale(self, element, timeout=None):
        local_wait = WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT)
        return local_wait.until(EC.staleness_of(element))
