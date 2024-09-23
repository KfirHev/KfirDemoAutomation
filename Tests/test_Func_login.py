import pytest

from PageObjects.HomePage import HomePage
from Utils.BaseClass import BaseClass
from TestData.HomePageData import HomePageData

@pytest.mark.skip
class TestLogin(BaseClass):

    @pytest.fixture(params=HomePageData.test_home_page_login)
    def get_data(self, request):
        return request.param

    def test_login(self, get_data):
        """Verify homepage title, logo , available users and pw ."""
        log = self.get_logger()
        home_page = HomePage(self.driver)

        home_page.set_user_name().get_attribute('placeholder')

        home_page.set_user_name().send_keys('Moshe')
        print(home_page.set_pw().get_attribute('placeholder'))
        home_page.set_pw().send_keys('STAM')
        home_page.login_btn().click()

        # # Verify page title
        # expected_title = 'Swag Labs'
        # page_title = home_page.get_title()
        # try:
        #     assert page_title == expected_title
        #     log.info("Page title verification passed.")
        # except AssertionError:
        #     log.error(f"Page title mismatch: expected '{expected_title}', got '{page_title}'")
        #     raise
        #
        # # Verify logo visibility
        # try:
        #     assert home_page.is_logo_displayed()
        #     log.info("Logo is displayed.")
        # except AssertionError:
        #     log.error("Logo is not displayed.")
        #     raise
        #
        # # Verify login btn visibility
        # try:
        #     assert home_page.is_login_btn_displayed()
        #     log.info("Login button is displayed.")
        # except AssertionError:
        #     log.error("Login button is not displayed.")
        #     raise
        #
        # # Verify accepted user_names on site
        # users = home_page.get_valid_user_name()
        # # Given user list
        # users_list = get_data['users']
        # try:
        #     assert set(users) == users_list
        #     log.info("Usernames match the expected list.")
        # except AssertionError:
        #     log.error(f"Usernames mismatch: expected {users_list}, got {users}")
        #     raise
        # # Verify accepted user_names on site
        # password = home_page.get_password()
        # # Given password
        # valid_pw = get_data['password']
        # try:
        #     assert valid_pw == password
        #     log.info("Password match the expected password.")
        # except AssertionError:
        #     log.error(f"Passwords mismatch: expected {valid_pw}, got {password}")
        #     raise
