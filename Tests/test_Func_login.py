import pytest
from PageObjects.HomePage import HomePage
from TestData.HomePageData import HomePageData
from Utils.BaseClass import BaseClass


class TestLogin(BaseClass):
    """
    This class tests the login functionality of the HomePage using valid credentials
    and verifies the flow from login to logout.
    """

    @pytest.fixture(params=HomePageData.test_home_page_login)
    def get_data(self, request):
        """
        Pytest fixture to get data for login tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_login(self, get_data):
        """
        Test the login and logout process for multiple valid users except the locked out user.

        The test asserts:
        - The page title after login is 'Products'
        - The page title after logout is 'Swag Labs'

        If any step fails, it logs the error and raises an exception.

        :param get_data: Test data for users and password.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        users = get_data['users']
        # Loop through all valid usernames except locked out user
        for user in users:
            if user != 'locked_out_user':
                try:
                    # Perform login
                    product_page = home_page.login(user, get_data['password'])
                    expected_products_title = 'Products'

                    # Assert the page title after login
                    assert expected_products_title == product_page.get_page_title()
                    log.info(f"Login with user {user} was successful.")

                    # Perform logout and assert the page title after logout
                    expected_home_page_title = 'Swag Labs'
                    home_page = product_page.log_out()
                    assert expected_home_page_title == home_page.get_title()
                    log.info(f"Logout from user {user} was successful.")

                except AssertionError as ae:
                    log.error(f"Assertion failed for user {user}: {str(ae)}")
                    raise

                except Exception as e:
                    log.error(f"Error during login/logout process for user {user}: {str(e)}")
                    raise

        # TODO add Negative tests get locator for err message and add it to the Homepage locators



