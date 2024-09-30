import time

import pytest
from PageObjects.HomePage import HomePage
from PageObjects.ProductsPage import ProductsPage
from TestData.ProductPageData import ProductPageData
from Utils.BaseClass import BaseClass


# @pytest.mark.skip
class TestProductsPage(BaseClass):
    """Tests for the Products Page functionality."""

    @pytest.fixture(params=ProductPageData.test_products)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_add_products_to_cart(self, get_data):
        """Test adding specified products to the cart and verify counts."""
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Extract necessary data
            product_name_from_data = get_data['product_names']
            number_of_products_to_add = len(product_name_from_data)

            log.info(f"Starting test with products: {product_name_from_data}")

            # Log into the application
            products_page = home_page.login('standard_user', 'secret_sauce')
            log.info("Login successful")

            # Get the product names displayed on the product page
            product_names = products_page.get_page_products_name()
            log.info(f"Products available on page: {product_names}")

            # Add specific products from the provided list
            products_page.add_product_to_cart(product_name_from_data)
            log.info(f"Added {product_name_from_data} to the cart")

            # Verify that the number of products added matches the cart icon count
            cart_icon_count = products_page.get_number_of_products_from_cart_icon()
            assert number_of_products_to_add == cart_icon_count, \
                f"Expected {number_of_products_to_add}, but found {cart_icon_count} on the cart icon"
            log.info(f"Number of products added to the cart icon is '{cart_icon_count}'")

            # Navigate to the cart and verify products in the cart
            cart_page = products_page.click_shopping_cart()
            products_in_cart = cart_page.get_page_products_name()
            log.info(f"Products in cart: {products_in_cart}")

            # Assert that the products in the cart match the expected list
            assert set(product_name_from_data) == set(products_in_cart), \
                f"Expected products in cart: {product_name_from_data}, but found: {products_in_cart}"
            log.info("All products successfully added to the cart")

            # Reset application state (clean up)
            cart_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")

        # TODO - do i need this function and the add all products from page ? or use only the data

        # # Add all products on product's page to the cart
        # products_page = home_page.login('standard_user', 'secret_sauce')
        # products_page.add_all_products_to_cart()
        # cart_page = products_page.click_shopping_cart()
        #
        # products_in_cart = cart_page.get_page_products_name()
        # assert set(product_names) == set(products_in_cart)
        # cart_page.reset_application_state()
