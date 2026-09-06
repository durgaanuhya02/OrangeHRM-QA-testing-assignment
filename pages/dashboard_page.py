"""
Page object for the OrangeHRM Dashboard and the top navigation bar
(main menu + user dropdown) that is present on every authenticated
page, since logging out is available from that shared bar.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    # --- Locators ---------------------------------------------------
    DASHBOARD_HEADER = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    # Main menu links carry a stable `href`, which survives UI theme
    # changes better than text or generated CSS classes.
    PIM_MENU_LINK = (By.CSS_SELECTOR, "a[href='/web/index.php/pim/viewPimModule']")
    USER_DROPDOWN_TAB = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/web/index.php/auth/logout']")

    def is_dashboard_displayed(self):
        self.wait_for_url_contains("dashboard")
        return self.get_text(self.DASHBOARD_HEADER) == "Dashboard"

    def navigate_to_pim(self):
        """Hovers over PIM (some OrangeHRM menu items reveal state /
        sub-items on hover) and then clicks it to open the module."""
        self.hover(self.PIM_MENU_LINK)
        self.click(self.PIM_MENU_LINK)
        self.wait_for_url_contains("pim")

    def logout(self):
        self.click(self.USER_DROPDOWN_TAB)
        self.click(self.LOGOUT_LINK)
        self.wait_for_url_contains("auth/login")
