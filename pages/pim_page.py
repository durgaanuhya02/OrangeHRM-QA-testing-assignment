"""
Page object for the PIM module landing area: the tab strip that
switches between "Employee List", "Add Employee" and "Reports".

At narrow window widths OrangeHRM collapses these tabs behind a
"More" toggle, so each navigation method first checks whether the
tab is already visible and only opens "More" when it isn't. Running
with a maximized window (see tests/conftest.py) keeps the tabs
visible directly in almost all cases, but this keeps the framework
resilient to smaller windows too.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.config import SHORT_TIMEOUT


class PIMPage(BasePage):
    # --- Locators ---------------------------------------------------
    PIM_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    MORE_TOGGLE = (By.XPATH, "//button[normalize-space()='More']")
    ADD_EMPLOYEE_TAB = (By.XPATH, "//a[normalize-space()='Add Employee']")
    EMPLOYEE_LIST_TAB = (By.XPATH, "//a[normalize-space()='Employee List']")

    def is_pim_page_displayed(self):
        self.wait_for_url_contains("pim")
        return self.get_text(self.PIM_HEADER) == "PIM"

    def _open_tab(self, tab_locator, url_fragment):
        try:
            # Short timeout here: if the tab is collapsed into "More"
            # this is expected to fail fast, not eat the full default wait.
            WebDriverWait(self.driver, SHORT_TIMEOUT).until(
                EC.element_to_be_clickable(tab_locator)
            ).click()
        except TimeoutException:
            # Tab strip is collapsed into "More" at this window width.
            self.click(self.MORE_TOGGLE)
            self.click(tab_locator)
        self.wait_for_url_contains(url_fragment)

    def click_add_employee(self):
        self._open_tab(self.ADD_EMPLOYEE_TAB, "addEmployee")

    def navigate_to_employee_list(self):
        self._open_tab(self.EMPLOYEE_LIST_TAB, "viewEmployeeList")
