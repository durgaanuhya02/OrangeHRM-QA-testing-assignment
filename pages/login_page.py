"""
Page object for the OrangeHRM Login page.
URL: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import LOGIN_URL


class LoginPage(BasePage):
    # --- Locators ---------------------------------------------------
    # `name` attributes are used where available since they are the
    # most stable locator OrangeHRM exposes for these fields.
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_ALERT = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    INVALID_FIELD_MESSAGE = (By.CSS_SELECTOR, ".oxd-input-group__message")
    # The demo page shows the valid credentials on-screen, e.g.
    # "Username : Admin" / "Password : admin123"
    DEMO_CREDENTIALS_TEXT = (By.CSS_SELECTOR, ".orangehrm-demo-credentials p")

    def open(self):
        self.driver.get(LOGIN_URL)
        self.find_visible(self.USERNAME_INPUT)
        return self

    def login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)

    def is_password_masked(self):
        return self.find_visible(self.PASSWORD_INPUT).get_attribute("type") == "password"

    def submit_with_enter_key(self, username, password):
        """Fills the form and submits by pressing Enter in the
        password field, instead of clicking the Login button."""
        from selenium.webdriver.common.keys import Keys

        self.type_text(self.USERNAME_INPUT, username)
        password_field = self.find_visible(self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)

    def get_displayed_credentials(self):
        """Reads the valid username/password shown on the login page
        itself, e.g. ['Username : Admin', 'Password : admin123'],
        and returns them as a dict: {'username': 'Admin', 'password': 'admin123'}."""
        lines = self.find_all(self.DEMO_CREDENTIALS_TEXT)
        creds = {}
        for line in lines:
            label, _, value = line.text.partition(":")
            creds[label.strip().lower()] = value.strip()
        return creds

    def get_error_message(self):
        return self.get_text(self.ERROR_ALERT)

    def is_login_page_displayed(self):
        return self.is_element_present(self.USERNAME_INPUT) and "auth/login" in self.driver.current_url

    def is_field_required_message_displayed(self):
        return self.is_element_present(self.INVALID_FIELD_MESSAGE, timeout=5)
