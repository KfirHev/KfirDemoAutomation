import time
import pytest
from PageObjects.HomePage import HomePage
from TestData.ProductPageData import ProductPageData
from Utils.BaseClass import BaseClass


@pytest.mark.skip
class TestProductPageSort(BaseClass):
    """Tests for the Products Page sorting functionality."""

    @pytest.fixture(params=ProductPageData.test_sorting_options)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_sorting_by_option(self, get_data):
        """
        Test the sorting functionality by name on the products page. The test performs the following actions:

        1. Logs into the application.
        2. Extracts the sorting option from the test data.
        3. Sorts the products using the selected sorting option.
        4. Verifies that the products are sorted correctly.
        5. Resets the application state after the test to ensure a clean environment for future tests.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Extract necessary data from the provided test data
            sort_option = get_data['option_name']
            log.info(f"Starting test with sort option: {sort_option}")

            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Sort products using the specified sorting option
            products_page.sort_products_by(sort_option)
            log.info(f"Products sorted by: {sort_option}")

            # Verify that the products are sorted correctly
            assert products_page.verify_sorting_is_correct(sort_option), \
                f"Sorting '{sort_option}' was unsuccessful"
            log.info(f"Sorting '{sort_option}' verified successfully")

            # Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise
