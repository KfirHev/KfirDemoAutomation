import pytest
import allure
import time
from PageObjects.HomePage import HomePage
from TestData.HomePageData import HomePageData
from Utils.BaseClass import BaseClass


@allure.feature("Login Process")
@allure.story("Login Latency Check")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.xfail
class TestLoginResponseTime(BaseClass):
    """
    This class tests the login response time for the HomePage using valid credentials.
    It verifies that the response time does not exceed the specified threshold (3 seconds).
    """
    MAX_RESPONSE_TIME = 3  # Maximum acceptable response time in seconds

    @pytest.fixture(params=HomePageData.test_login_latency)
    def get_data(self, request):
        """
        Pytest fixture to parameterize test data for login tests.

        :param request: The request object provided by pytest, which includes
                        the parameterized data for the test method.
        :return: Returns a dictionary containing test data for users and passwords.
        """
        return request.param

    def test_login_response_time(self, get_data):
        """
        Test the login process for multiple valid users and assert that the login response time
        does not exceed the defined maximum response time.

        The test logs the response time for each user and collects failures if any user exceeds
        the allowed response time. At the end of the test, it asserts whether any failures occurred.

        :param get_data: A dictionary containing test data for users and passwords.
        """
        log = self.get_logger()  # Retrieve the logger instance
        home_page = HomePage(self.driver)  # Instantiate the HomePage object

        users = get_data['users']  # Get the list of users from the test data
        failures = []  # List to store any failures encountered during the test

        # Loop through each valid username provided in the test data
        for user in users:
            try:
                # Capture the start time before performing the login
                start_time = time.time()

                # Attempt to log in using the current user's credentials
                product_page = home_page.login(user, get_data['password'])

                # Capture the end time after login attempt
                end_time = time.time()

                # Calculate the response time taken for the login process
                login_response_time = round((end_time - start_time), 3)
                log.info(f"Login response time for user {user}: {login_response_time} seconds")

                # Check if the calculated response time exceeds the maximum allowable response time
                if login_response_time > self.MAX_RESPONSE_TIME:
                    failures.append(f"Login response time exceeded {self.MAX_RESPONSE_TIME} seconds for "
                                    f"user {user}: {login_response_time} seconds.")

                # Perform logout after successful login
                product_page.reset_application_state()

            except Exception as e:
                # Log any errors encountered during the login process
                failures.append(f"Error during login process for user {user}: {str(e)}")

        # At the end of the test, assert if any failures were recorded
        if failures:
            log.error(f"Failures detected:\n{"\n".join(failures)}")  # Log all failures
            assert False, "Test failed for the following users:\n" + "\n".join(failures)  # Fail the test
