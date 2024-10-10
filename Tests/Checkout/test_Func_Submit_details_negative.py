import time

import pytest
from PageObjects.HomePage import HomePage
from TestData.CheckOutInfoPageData import CheckOutInfoPageData
from Utils.BaseClass import BaseClass


# @pytest.mark.skip
class TestSubmitData(BaseClass):
    """Tests for the Products Page remove functionality."""

    @pytest.fixture(params=CheckOutInfoPageData.test_submit_page)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_submit_info_negative(self, get_data):

        log = self.get_logger()
        home_page = HomePage(self.driver)

        # Extract necessary data

        expected_error_messages = get_data['expected_error_messages']

        try:

            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            products_page.add_all_products_to_cart()
            products_page.click_shopping_cart()
            checkout_info_page = products_page.checkout()

            checkout_info_page.submit_info(first_name='', last_name='', postal='')

            error_message = checkout_info_page.get_submit_error_message()
            assert error_message == expected_error_messages['empty_name'], \
                (f"Checkout info submission was unsuccessful expected '{expected_error_messages['empty_name']}"
                 f"' got '{error_message}'")
            log.info(
                f"Submit without first name failed as expected with message: {error_message}")

            checkout_info_page.clear_submit_error_message()

            checkout_info_page.submit_info(first_name='Shay', last_name='', postal='')
            error_message = checkout_info_page.get_submit_error_message()
            assert error_message == expected_error_messages['empty_last_name'], \
                (f"Checkout info submission was unsuccessful expected '{expected_error_messages['empty_last_name']}"
                 f"' got '{error_message}'")
            log.info(
                f"Submit without last name failed as expected with message: {error_message}")
            checkout_info_page.clear_submit_error_message()

            checkout_info_page.submit_info(first_name='Mor', last_name='Gold', postal='')
            error_message = checkout_info_page.get_submit_error_message()
            assert error_message == expected_error_messages['empty_postal'], \
                (f"Checkout info submission was unsuccessful expected '{expected_error_messages['empty_postal']}"
                 f"' got '{error_message}'")
            log.info(
                f"Submit without postal code failed as expected with message: {error_message}")

            # Reset the application state to avoid side effects on other tests
            checkout_info_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise
