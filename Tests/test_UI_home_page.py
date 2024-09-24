import pytest

from PageObjects.HomePage import HomePage
from Utils.BaseClass import BaseClass
from TestData.HomePageData import HomePageData


@pytest.mark.skip
class TestHomePage(BaseClass):
    """Test suite for the Home Page of the application."""

    @pytest.fixture(params=HomePageData.test_home_page_login)
    def get_data(self, request):
        """Fixture to provide test data for the login page.

        :param request: The request object for accessing the parameter.
        :return: A dictionary containing user login data.
        """
        return request.param

    def test_landing_page(self, get_data):
        """Verify homepage title, logo, hints, available users, and sites password.

        :param get_data: The test data provided by the fixture.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        # Verify page title
        expected_title = 'Swag Labs'
        page_title = home_page.get_title()
        try:
            assert page_title == expected_title
            log.info("Page title verification passed.")
        except AssertionError:
            log.error(f"Page title mismatch: expected '{expected_title}', got '{page_title}'")
            raise

        # Verify logo visibility
        try:
            assert home_page.is_logo_displayed()
            log.info("Logo is displayed.")
        except AssertionError:
            log.error("Logo is not displayed.")
            raise

        # Verify login button visibility
        try:
            assert home_page.is_login_btn_displayed()
            log.info("Login button is displayed.")
        except AssertionError:
            log.error("Login button is not displayed.")
            raise

        # Validate Username hint
        user_hint = home_page.get_user_hint()
        expected_user_hint = get_data['user_name_hint']
        try:
            assert user_hint == expected_user_hint
            log.info("User hint is as expected.")
        except AssertionError:
            log.error(f"User hint mismatch: expected {expected_user_hint}, got {user_hint}")
            raise

        # Validate Password hint
        pw_hint = home_page.get_password_hint()
        expected_pw_hint = get_data['pw_hint']
        try:
            assert pw_hint == expected_pw_hint
            log.info("Password hint is as expected.")
        except AssertionError:
            log.error(f"Password hint mismatch: expected {expected_pw_hint}, got {pw_hint}")
            raise

        # Verify accepted usernames on site
        users = home_page.get_valid_user_name()
        users_list = get_data['users']
        try:
            assert set(users) == set(users_list)
            log.info("Usernames match the expected list.")
        except AssertionError:
            log.error(f"Usernames mismatch: expected {users_list}, got {users}")
            raise

        # Verify accepted password
        password = home_page.get_password()
        valid_pw = get_data['password']
        try:
            assert valid_pw == password
            log.info("Password matches the expected password.")
        except AssertionError:
            log.error(f"Passwords mismatch: expected {valid_pw}, got {password}")
            raise
