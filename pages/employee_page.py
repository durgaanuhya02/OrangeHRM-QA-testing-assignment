"""
Page object covering both the "Add Employee" form and the
"Employee List" search/results screen, since they share the same
PIM data model and are used together by the employee-management
workflow (create an employee, then find it again).
"""

import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.config import LONG_TIMEOUT


class EmployeePage(BasePage):
    # --- Add Employee form locators ---------------------------------
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    MIDDLE_NAME_INPUT = (By.NAME, "middleName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    # OrangeHRM auto-suggests this ID; it has no name/id attribute.
    EMPLOYEE_ID_INPUT = (
        By.XPATH,
        "//label[text()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    # NOTE: `.` (the element's full string-value) is used instead of
    # `text()` throughout this file. Vue splits interpolated content
    # like "{{ count }} Record Found" into separate sibling text
    # nodes, and XPath's contains(text(), ...) only ever looks at the
    # FIRST text node -- it silently misses text spread across more
    # than one, which `contains(., ...)` does not.
    EMPLOYEE_ID_EXISTS_ERROR = (
        By.XPATH,
        "//*[contains(., 'Employee Id already exists')]",
    )
    SAVE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # --- Employee List search locators ------------------------------
    # The "Employee Name" autocomplete field is reached via its label
    # because the input itself has no name/id, only a shared
    # placeholder ("Type for hints...") also used by "Supervisor Name".
    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//label[text()='Employee Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    AUTOCOMPLETE_OPTION = (By.CSS_SELECTOR, "div.oxd-autocomplete-option")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    # Scoped to the results-count span (not a bare //*) so this can't
    # accidentally match the similarly-worded "No Records Found" toast
    # popup that briefly appears elsewhere on the page.
    RECORD_COUNT_TEXT = (
        By.XPATH,
        "//span[contains(@class,'oxd-text--span')][contains(., 'Record') and contains(., 'Found')]",
    )
    TABLE_CELLS = (By.CSS_SELECTOR, ".oxd-table-cell")
    NO_RECORDS_MESSAGE = (
        By.XPATH,
        "//span[contains(@class,'oxd-text--span')][contains(., 'No Records Found')]",
    )

    # ------------------------------------------------------------------
    # Add Employee
    # ------------------------------------------------------------------
    def add_employee(self, first_name, middle_name, last_name, max_attempts=5):
        """Fills and saves the Add Employee form. Returns the new
        employee's numeric ID, parsed from the post-save URL
        (".../pim/viewPersonalDetails/empNumber/<id>"), which is the
        most reliable proof that OrangeHRM actually created the
        record (a validation error would leave the URL unchanged).

        OrangeHRM auto-suggests an Employee Id, but on the shared
        public demo instance other testers are creating employees at
        the same time, so that suggested Id can already be taken by
        the time we submit. If the "Employee Id already exists"
        validation appears, this retries with a randomised Id instead
        of failing the whole test over a data clash that has nothing
        to do with the feature being tested.
        """
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        if middle_name:
            self.type_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)

        for attempt in range(1, max_attempts + 1):
            self.click(self.SAVE_BUTTON)
            try:
                self.wait_for_url_contains("viewPersonalDetails", timeout=8)
                return self.driver.current_url.rstrip("/").split("/")[-1]
            except Exception:
                if attempt == max_attempts or not self.is_element_present(
                    self.EMPLOYEE_ID_EXISTS_ERROR, timeout=3
                ):
                    raise
                new_id = str(random.randint(100000, 999999))
                self.type_text(self.EMPLOYEE_ID_INPUT, new_id)

        raise AssertionError("Could not save employee after retrying with a new Employee Id")

    def is_employee_created(self):
        return "viewPersonalDetails" in self.driver.current_url

    # ------------------------------------------------------------------
    # Employee List search & verification
    # ------------------------------------------------------------------
    def search_employee(self, full_name):
        """Types the employee's full name into the Employee Name
        autocomplete field, selects the matching suggestion (falls
        back to a plain search if no suggestion appears -- e.g. if
        the demo data changed), and runs the search."""
        self.type_text(self.EMPLOYEE_NAME_INPUT, full_name)
        try:
            option = self.wait.until(
                EC.visibility_of_element_located(self.AUTOCOMPLETE_OPTION)
            )
            option.click()
        except Exception:
            pass  # proceed with the typed text as-is
        self.click(self.SEARCH_BUTTON)
        # Either a result count or a "no records" message will appear.
        # A longer timeout is used here because the shared public demo
        # can be slow to respond to the search request under load.
        WebDriverWait(self.driver, LONG_TIMEOUT).until(
            EC.any_of(
                EC.presence_of_element_located(self.RECORD_COUNT_TEXT),
                EC.presence_of_element_located(self.NO_RECORDS_MESSAGE),
            )
        )

    def verify_employee(self, full_name):
        """Returns True if every word of `full_name` appears somewhere
        in the results table after search_employee() has been called.

        The table splits a name across two columns -- "First (&
        Middle) Name" and "Last Name" -- so the full name is never
        sitting in a single cell as one string. All cell texts are
        joined together first and each word is checked against that,
        rather than looking for the whole name in one cell."""
        if self.is_element_present(self.NO_RECORDS_MESSAGE, timeout=3):
            return False
        cells = self.find_all(self.TABLE_CELLS)
        combined_row_text = " ".join(cell.text.strip() for cell in cells)
        return all(word in combined_row_text for word in full_name.split())
