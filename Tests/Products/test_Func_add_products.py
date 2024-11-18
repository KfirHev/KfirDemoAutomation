import time
import pytest
import allure
from PageObjects.HomePage import HomePage
from TestData.ProductPageData import ProductPageData
from Utils.BaseClass import BaseClass


#@pytest.mark.skip
@allure.feature("Product Add")
@allure.story("Add Products Check")
@allure.severity(allure.severity_level.CRITICAL)
class TestProductsPageAdd(BaseClass):
    """Tests for the Products Page add functionality."""

    @pytest.fixture(params=ProductPageData.test_products)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_add_products_to_cart(self, get_data):
        """
        Test the process of adding specified products to the shopping cart and
        verifying that the product counts reflect the expected results. This test
        ensures that the following functionalities work as intended:

        1. Logging into the application successfully.
        2. Retrieving the list of available products from the product page.
        3. Adding specific products to the shopping cart based on provided data.
        4. Validating that the number of items in the cart matches the count of
           products added.
        5. Navigating to the cart and confirming that the products displayed match
           the expected products.
        6. Cleaning up the application state after the test is complete to ensure
           no residual data affects subsequent tests.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Extract necessary data from the provided test data
            product_name_from_data = get_data['product_names']
            number_of_products_to_add = len(product_name_from_data)

            log.info(f"Starting test with products: {product_name_from_data}")

            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Retrieve the names of products currently displayed on the product page
            product_names = products_page.get_page_products_name()
            log.info(f"Products available on page: {product_names}")

            # Add the specified products to the shopping cart
            products_page.add_product_to_cart(product_name_from_data)
            log.info(f"Added {product_name_from_data} to the cart")

            # Verify that the number of products added matches the count displayed on the cart icon
            cart_icon_count = products_page.get_number_of_products_from_cart_icon()
            assert number_of_products_to_add == cart_icon_count, \
                f"Expected {number_of_products_to_add}, but found {cart_icon_count} on the cart icon"
            log.info(f"Number of products added to the cart icon is '{cart_icon_count}'")

            # Navigate to the shopping cart and retrieve the products listed there
            cart_page = products_page.click_shopping_cart()
            products_in_cart = cart_page.get_page_products_name()
            log.info(f"Products in cart: {products_in_cart}")

            # Assert that the products in the cart match the expected products
            assert set(product_name_from_data) == set(products_in_cart), \
                f"Expected products in cart: {product_name_from_data}, but found: {products_in_cart}"
            log.info("All products successfully added to the cart")

            # Reset the application state (clean up) to avoid side effects on other tests
            cart_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise

