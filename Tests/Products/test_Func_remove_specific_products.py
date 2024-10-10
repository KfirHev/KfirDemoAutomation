import time

import pytest
from PageObjects.HomePage import HomePage
from TestData.SingleProductPageData import SingleProductPageData
from Utils.BaseClass import BaseClass


@pytest.mark.skip
class TestSingleProductsPageRemove(BaseClass):
    """Tests for the Products Page remove functionality."""

    @pytest.fixture(params=SingleProductPageData.test_single_product)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_remove_products_from_cart(self, get_data):
        """
        Test the functionality of removing a specific product from the cart and verifying
        that the cart count decreases. The test performs the following actions:

        1. Logs into the application.
        2. Adds all products on the page to the cart.
        3. Removes a specified product from the cart.
        4. Verifies that the product count in the cart has decreased.
        5. Resets the application state to ensure a clean environment for future tests.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Extract the product name from the test data
            product_name = get_data['product_name']
            log.info(f"Starting test with product: {product_name}")

            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Add all products on the page
            products_page.add_all_products_to_cart()
            log.info(f"Added all page's products to the cart")

            # Count the current number of products in the cart
            initial_product_count = products_page.get_number_of_products_from_cart_icon()
            log.info(f"Initial product count in the cart: {initial_product_count}")

            # Click on the product to view its details
            single_product_page = products_page.click_product_by_name(product_name)

            # Remove the product from the cart
            single_product_page.remove_product_from_cart()
            log.info(f"Removed {product_name} from the cart")

            # Verify that the product has been removed
            cart_icon_count = products_page.get_number_of_products_from_cart_icon()
            assert cart_icon_count == initial_product_count - 1, \
                f"Expected one less product, but found {cart_icon_count} in the cart"
            log.info(f"Number of products in the cart icon is '{cart_icon_count}'")

            # Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise

