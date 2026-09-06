"""
Central configuration for the OrangeHRM automation suite.
Keeping URLs, timeouts and test data here means a locator or
environment change only needs to be made in one place.
"""

import os

# --- Application URLs -------------------------------------------------
BASE_URL = "https://opensource-demo.orangehrmlive.com"
LOGIN_URL = f"{BASE_URL}/web/index.php/auth/login"

# --- Timeouts (seconds) -------------------------------------------------
DEFAULT_TIMEOUT = 15
SHORT_TIMEOUT = 5
# The public demo can be noticeably slower under load (many people
# testing against it concurrently) than a private test environment,
# so a few waits that were observed timing out right around 15s use
# this longer budget instead of tightening the whole framework.
LONG_TIMEOUT = 25

# --- Browser -------------------------------------------------
# Overridable via environment variable, e.g. `set BROWSER=firefox`
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# --- Directories -------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")

# --- Test data -------------------------------------------------
# NOTE: The OrangeHRM demo login page displays valid credentials
# directly on screen. LoginPage.get_displayed_credentials() reads
# them at runtime, but these constants are kept as a documented
# fallback/reference for anyone reading the test data.
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"

INVALID_USERNAME = "InvalidUser123"
INVALID_PASSWORD = "WrongPass123"

# Employees created and verified by test_employee_management.py.
# The last name is a template only -- tests/conftest.py appends a
# unique run ID to it at runtime so repeated runs against the shared
# public demo instance never collide with employees created earlier.
EMPLOYEE_TEMPLATES = [
    {"first_name": "Ananya", "middle_name": "QA", "last_name": "Tester"},
    {"first_name": "Rahul", "middle_name": "Automation", "last_name": "Tester"},
    {"first_name": "Priya", "middle_name": "Selenium", "last_name": "Tester"},
    {"first_name": "Arjun", "middle_name": "POM", "last_name": "Tester"},
]
