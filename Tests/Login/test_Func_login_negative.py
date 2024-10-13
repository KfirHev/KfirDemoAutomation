import pytest
from PageObjects.HomePage import HomePage
from TestData.HomePageData import HomePageData
from Utils.BaseClass import BaseClass

@pytest.mark.skip
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

    @staticmethod
    def login_and_verify_error(home_page, username, password, expected_error, log):
        """
        Helper method to perform login, capture error message, and verify with expected error.

        :param home_page: HomePage object to perform login actions.
        :param username: Username for login attempt.
        :param password: Password for login attempt.
        :param expected_error: Expected error message to assert.
        :param log: Logger object for logging.
        """
        try:
            home_page.login(username, password)
            error_message = home_page.get_login_error_message()

            # Assert the actual error message matches the expected one
            assert error_message == expected_error, \
                f"Unexpected error message for user '{username}' or password '{password}'"

            log.info(
                f"Login with user '{username}' and password '{password}' failed as expected with message: {expected_error}")

            # Clear the error message after the test
            home_page.clear_login_error_message()

        except AssertionError as ae:
            log.error(f"Assertion failed for user '{username}': {str(ae)}")
            raise
        except Exception as e:
            log.error(f"Error during invalid login process for user '{username}': {str(e)}")
            raise

    def test_login_negative(self, get_data):
        log = self.get_logger()
        home_page = HomePage(self.driver)

        # Extract necessary data
        valid_user = get_data['users']
        invalid_users = get_data['invalid_users']
        expected_error_messages = get_data['expected_error_messages']
        password = get_data['password']
        invalid_passwords = get_data['invalid_passwords']
        locked_user = get_data['locked_user']

        # Test login without username
        self.login_and_verify_error(home_page, '', '',
                                    expected_error_messages['empty_username'], log)

        # Test login without password
        self.login_and_verify_error(home_page, valid_user[0], '',
                                    expected_error_messages['empty_password'], log)

        # Loop through all invalid usernames and check error is as expected
        for user in invalid_users:
            self.login_and_verify_error(home_page, user, password,
                                        expected_error_messages['invalid_credentials'], log)

        # Loop through invalid passwords and check error is as expected
        for pw in invalid_passwords:
            self.login_and_verify_error(home_page, valid_user[0], pw,
                                        expected_error_messages['invalid_credentials'],
                                        log)

        # Test login with locked user
        self.login_and_verify_error(home_page, locked_user, password,
                                    expected_error_messages['locked_user'], log)
