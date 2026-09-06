"""
Automated regression coverage for the login page.

These tests automate a practical subset of the manual login test
cases in docs/manual_test_cases_login.md -- the ones that produce a
deterministic, UI-checkable outcome. A few manual cases (e.g. account
lockout after many failed attempts, or password case-sensitivity)
are intentionally NOT automated here because they would require
mutating the shared public demo's admin account, which would affect
every other person testing against it.
"""

import pytest

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.config import INVALID_USERNAME, INVALID_PASSWORD


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).open()


def test_valid_login_displays_dashboard(driver, login_page):
    """TC_LOGIN_01: valid username + valid password logs in successfully."""
    creds = login_page.get_displayed_credentials()
    login_page.login(creds["username"], creds["password"])

    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed(), "Dashboard was not displayed after a valid login"


def test_invalid_username_valid_password(driver, login_page):
    """TC_LOGIN_02: invalid username + valid password is rejected."""
    creds = login_page.get_displayed_credentials()
    login_page.login(INVALID_USERNAME, creds["password"])

    assert login_page.get_error_message() == "Invalid credentials"
    assert login_page.is_login_page_displayed()


def test_valid_username_invalid_password(driver, login_page):
    """TC_LOGIN_03: valid username + invalid password is rejected."""
    creds = login_page.get_displayed_credentials()
    login_page.login(creds["username"], INVALID_PASSWORD)

    assert login_page.get_error_message() == "Invalid credentials"
    assert login_page.is_login_page_displayed()


def test_invalid_username_and_password(driver, login_page):
    """TC_LOGIN_04: invalid username + invalid password is rejected."""
    login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

    assert login_page.get_error_message() == "Invalid credentials"
    assert login_page.is_login_page_displayed()


def test_empty_username_and_password(driver, login_page):
    """TC_LOGIN_05: submitting the form with both fields empty shows
    inline 'Required' validation and does not navigate away."""
    login_page.click_login_button()

    assert login_page.is_field_required_message_displayed()
    assert login_page.is_login_page_displayed()


def test_empty_username_only(driver, login_page):
    """TC_LOGIN_06: empty username with a password filled in is
    blocked by the same inline required-field validation."""
    creds = login_page.get_displayed_credentials()
    login_page.type_text(login_page.PASSWORD_INPUT, creds["password"])
    login_page.click_login_button()

    assert login_page.is_field_required_message_displayed()
    assert login_page.is_login_page_displayed()


def test_empty_password_only(driver, login_page):
    """TC_LOGIN_07: empty password with a username filled in is
    blocked by the same inline required-field validation."""
    creds = login_page.get_displayed_credentials()
    login_page.type_text(login_page.USERNAME_INPUT, creds["username"])
    login_page.click_login_button()

    assert login_page.is_field_required_message_displayed()
    assert login_page.is_login_page_displayed()


def test_username_with_leading_and_trailing_spaces_is_rejected(driver, login_page):
    """TC_LOGIN_08: a valid username padded with whitespace is treated
    as a different (invalid) value -- OrangeHRM does not trim it."""
    creds = login_page.get_displayed_credentials()
    login_page.login(f"  {creds['username']}  ", creds["password"])

    assert login_page.get_error_message() == "Invalid credentials"
    assert login_page.is_login_page_displayed()


def test_password_field_masks_input(driver, login_page):
    """TC_LOGIN_09: the password field must render as type='password'
    so the value is masked on screen."""
    assert login_page.is_password_masked()


def test_username_is_case_insensitive(driver, login_page):
    """TC_LOGIN_10: logging in with a lower-cased version of the valid
    username still succeeds (verified behavior, not assumed)."""
    creds = login_page.get_displayed_credentials()
    login_page.login(creds["username"].lower(), creds["password"])

    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()


def test_login_submission_with_enter_key(driver, login_page):
    """TC_LOGIN_11: pressing Enter in the password field submits the
    form the same way clicking Login does."""
    creds = login_page.get_displayed_credentials()
    login_page.submit_with_enter_key(creds["username"], creds["password"])

    dashboard = DashboardPage(driver)
    assert dashboard.is_dashboard_displayed()
