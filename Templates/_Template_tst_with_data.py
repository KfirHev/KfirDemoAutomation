import time

import pytest
from PageObjects.HomePage import HomePage
from TestData.SingleProductPageData import SingleProductPageData
from Utils.BaseClass import BaseClass


# @pytest.mark.skip
class Name_TestSingleProductsPageRemove(BaseClass):
    """Tests for the Products Page remove functionality."""

    @pytest.fixture(params=SingleProductPageData.test_single_product)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_name_(self, get_data):

        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:

            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")

