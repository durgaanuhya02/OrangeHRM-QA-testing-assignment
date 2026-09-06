"""
End-to-end workflow: log in, open PIM, add several employees,
verify every one of them in the Employee List, then log out.

This mirrors the exact assignment workflow rather than testing each
piece in isolation, because the steps are naturally sequential (you
cannot verify an employee that hasn't been created yet).
"""

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PIMPage
from pages.employee_page import EmployeePage


def test_add_and_verify_multiple_employees(driver, employees_data):
    login_page = LoginPage(driver).open()
    dashboard_page = DashboardPage(driver)
    pim_page = PIMPage(driver)
    employee_page = EmployeePage(driver)

    # --- Step 1: Login -------------------------------------------------
    creds = login_page.get_displayed_credentials()
    login_page.login(creds["username"], creds["password"])
    assert dashboard_page.is_dashboard_displayed(), "Login did not land on the Dashboard"

    # --- Step 2: Navigate to PIM ----------------------------------------
    dashboard_page.navigate_to_pim()
    assert pim_page.is_pim_page_displayed(), "PIM module did not open"

    # --- Step 3: Add employees, keeping their full names for later -----
    created_employee_names = []
    for employee in employees_data:
        pim_page.click_add_employee()
        employee_id = employee_page.add_employee(
            employee["first_name"], employee["middle_name"], employee["last_name"]
        )
        assert employee_page.is_employee_created(), (
            f"Employee {employee['first_name']} {employee['last_name']} was not created"
        )
        print(f"Created employee ID {employee_id}: "
              f"{employee['first_name']} {employee['middle_name']} {employee['last_name']}")

        full_name = f"{employee['first_name']} {employee['last_name']}"
        created_employee_names.append(full_name)

    # --- Step 4: Verify every created employee in the Employee List -----
    pim_page.navigate_to_employee_list()
    for full_name in created_employee_names:
        employee_page.search_employee(full_name)
        found = employee_page.verify_employee(full_name)
        assert found, f"Employee '{full_name}' was NOT found in the Employee List"
        print("Name Verified")

    # --- Step 5: Logout --------------------------------------------------
    dashboard_page.logout()
    assert login_page.is_login_page_displayed(), "Logout did not return to the Login page"
