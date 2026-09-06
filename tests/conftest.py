"""
Shared pytest fixtures: WebDriver lifecycle, unique per-run test
data, and automatic screenshots on test failure.
"""

import os
import time
import copy

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.config import HEADLESS, SCREENSHOTS_DIR, EMPLOYEE_TEMPLATES


@pytest.fixture(scope="function")
def driver():
    """Creates a fresh Chrome WebDriver for each test function and
    guarantees it is closed afterwards, even if the test fails."""
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=options)
    chrome_driver.maximize_window()

    yield chrome_driver

    chrome_driver.quit()


@pytest.fixture(scope="session")
def run_id():
    """A short, unique suffix for this test session, used to keep
    employee names unique across repeated runs against the shared
    public OrangeHRM demo instance."""
    return str(int(time.time()))


@pytest.fixture
def employees_data(run_id):
    """Returns the employee test data with the run ID appended to
    each last name, e.g. 'Tester1717000000', so re-running the suite
    never creates a name collision with a previous run's employees."""
    data = copy.deepcopy(EMPLOYEE_TEMPLATES)
    for employee in data:
        employee["last_name"] = f"{employee['last_name']}{run_id}"
    return data


# ----------------------------------------------------------------------
# Screenshot on failure
# ----------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each test phase, checks whether it failed and, if the
    test used the `driver` fixture, saves a screenshot named after
    the test for easier debugging."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture is not None:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            safe_name = item.name.replace("[", "_").replace("]", "_")
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot_path = os.path.join(
                SCREENSHOTS_DIR, f"FAILED_{safe_name}_{timestamp}.png"
            )
            try:
                driver_fixture.save_screenshot(screenshot_path)
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as exc:
                print(f"\nCould not capture screenshot: {exc}")
