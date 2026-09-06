 1. Project Overview
This project is a QA/SDET assignment covering both **manual testing** and **test automation** for the [OrangeHRM Open Source Demo](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login) application. It includes documented manual test cases, potential bug/usability observations, and a Python + Selenium automation framework built with the Page Object Model (POM).

 2. Objective
- Design and document manual test cases for the Login page and the Employee Management (PIM) module.
- Identify and clearly label potential bugs/usability issues on the login page, without overstating them as confirmed defects.
- Build a maintainable Selenium automation framework (POM, explicit waits, pytest, screenshots on failure) that automates the core login and employee-management workflows.

 3. Application Under Test
- **Application:** OrangeHRM Open Source Demo
- **URL:** https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
- **Credentials:** Displayed directly on the login page (`Username : Admin` / `Password : admin123`). The automation reads these from the page at runtime rather than hard-coding them as secrets — see `LoginPage.get_displayed_credentials()`.

4. Tools & Technologies
| Tool | Purpose |
|---|---|
| Python 3 | Automation language |
| Selenium WebDriver 4.x | Browser automation |
| pytest | Test runner & assertions |
| webdriver-manager | Automatic ChromeDriver installation/management |
| Page Object Model (POM) | Automation design pattern |

5. Project Structure
orangehrm-qa/
│
├── pages/                       # Page Object Model classes
│   ├── base_page.py             # Shared explicit-wait/interaction helpers
│   ├── login_page.py            # Login page locators + actions
│   ├── dashboard_page.py        # Dashboard + top nav (PIM link, logout)
│   ├── pim_page.py              # PIM tab navigation (Add Employee / Employee List)
│   └── employee_page.py         # Add Employee form + Employee List search/verify
│
├── tests/
│   ├── conftest.py              # WebDriver fixture, unique test data, screenshot-on-failure
│   ├── test_login.py            # 11 automated login test cases
│   └── test_employee_management.py  # End-to-end add/verify/logout workflow
│
├── utils/
│   └── config.py                # URLs, timeouts, test data templates
│
├── docs/
│   ├── manual_test_cases_login.md
│   ├── manual_test_cases_employee_management.md
│   ├── bug_reports.md
│   ├── github_setup.md
│   └── loom_script.md
│
├── screenshots/                 # Auto-populated on test failure
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

6. Prerequisites
- Python 3.9+
- Google Chrome installed
- Internet access (tests run against the live public demo site)

 7. Installation

```bash
cd orangehrm-qa
pip install -r requirements.txt
```

No manual ChromeDriver download is needed — `webdriver-manager` downloads the correct driver version for your installed Chrome automatically the first time you run the tests.

8. How to Run Tests

Run the full suite:
```bash
pytest
```

Run only the login tests:
```bash
pytest tests/test_login.py
```

Run only the employee management workflow:
```bash
pytest tests/test_employee_management.py
```

Run a single test by name:
```bash
pytest tests/test_login.py::test_valid_login_displays_dashboard
```

Expected output
Each test prints its name followed by `PASSED` or `FAILED` (the project's `pytest.ini` enables verbose, no-capture output, so `print()` statements in the tests — like `Name Verified` — are visible in the console). A full passing run of `test_employee_management.py` looks like:

```
tests/test_employee_management.py::test_add_and_verify_multiple_employees
Created employee ID 259: Ananya QA Tester...
Created employee ID 262: Rahul Automation Tester...
Created employee ID 264: Priya Selenium Tester...
Created employee ID 265: Arjun POM Tester...
Name Verified
Name Verified
Name Verified
Name Verified
PASSED
```

If any test fails, a screenshot is automatically saved to `screenshots/FAILED_<test_name>_<timestamp>.png`.

9. Test Scenarios
See [`docs/manual_test_cases_login.md`](docs/manual_test_cases_login.md) (15 cases) and [`docs/manual_test_cases_employee_management.md`](docs/manual_test_cases_employee_management.md) (13 cases) for the full manual test documentation, and [`docs/bug_reports.md`](docs/bug_reports.md) for the three potential login-page issues identified.

10. Automation Workflow
The automated suite covers:
1. **Login** — using the credentials displayed on the page, verifying the Dashboard loads.
2. **Navigate to PIM** — via the main menu (with a hover step, since some OrangeHRM menu items reveal state on hover).
3. **Add employees** — 4 employees with unique, timestamp-suffixed names (`Ananya QA Tester<id>`, `Rahul Automation Tester<id>`, `Priya Selenium Tester<id>`, `Arjun POM Tester<id>`), created one after another.
4. **Verify employees** — each created employee is searched for in the Employee List and confirmed present; `"Name Verified"` is printed for each successful match, and the assertion fails with a clear message if one is missing.
5. **Logout** — via the user dropdown menu, with a final assertion that the Login page is displayed again.

11. POM Architecture
- **`base_page.py`** holds only generic Selenium mechanics (explicit waits, click/type helpers) — no business logic or page-specific locators.
- Each page class (`LoginPage`, `DashboardPage`, `PIMPage`, `EmployeePage`) owns its own locators and exposes intention-revealing methods (`login()`, `navigate_to_pim()`, `add_employee()`, `search_employee()`, `verify_employee()`, `logout()`) — tests call these methods and assert on their results; they never touch a `By.XPATH` locator directly.
- Locators prefer `By.NAME`/`By.CSS_SELECTOR` on stable attributes (e.g. `name="firstName"`, `href="/web/index.php/pim/viewPimModule"`) and fall back to scoped XPath only where OrangeHRM's UI genuinely has no better handle (e.g. the Employee Name autocomplete field, which has no `name`/`id`).

 12. Expected Results
All 11 login tests and the employee-management workflow pass against the live demo site as of the date this project was built (verified by directly running `pytest` against `opensource-demo.orangehrmlive.com` during development — see Known Limitations for why an occasional re-run may be needed).

 13. Known Limitations
- Shared public demo instance:`opensource-demo.orangehrmlive.com` is used by many people simultaneously. This caused two real issues during development, both of which the framework now handles:
  - The **auto-suggested Employee Id can collide with a record someone else just created — `EmployeePage.add_employee()` detects the "Employee Id already exists" error and retries with a random Id.
  - The site can be **slower than usual** under concurrent load — the Employee List search wait uses a longer timeout (`LONG_TIMEOUT`, 25s) than the framework default (15s) for this reason.
- **Occasional transient failures:** because this suite runs against a live, shared, third-party-hosted demo (not a private test environment), a single test may occasionally fail due to network latency or site load and pass on re-run. This was observed once during development (`test_invalid_username_valid_password`) and confirmed to pass on retry — it was not a framework defect.
- **Account lockout / rate-limiting was intentionally not tested**, since repeated failed logins against the shared `Admin` account could disrupt other people testing against the same instance (see `docs/bug_reports.md`, BUG_003).
- **Some manual test cases are marked "To be verified"** rather than given an assumed result, per the assignment's instruction not to invent application behavior — see the manual test case documents for the full list and the reasoning behind each.
- Test data (employee names) accumulates on the shared demo over time since there is no automated teardown/deletion after the test run; this is intentional, to avoid deleting other testers' concurrent work by mistake.

## 14. Author
G DURGA ANUHYA
anuhya0202@gmail.com
