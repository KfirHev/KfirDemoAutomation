import time

import pytest
from PageObjects.HomePage import HomePage
from TestData.SingleProductPageData import SingleProductPageData
from Utils.BaseClass import BaseClass


@pytest.mark.skip
class TestSingleProductPageAdd(BaseClass):
    """Tests for the Single products Page functionality."""

    @pytest.fixture(params=SingleProductPageData.test_single_product)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_add_products_to_cart_specific(self, get_data):
        """
        Test the functionality of adding a specified single product to the cart and
        verifying that the cart count reflects the addition. The test performs the
        following actions:

        1. Logs into the application.
        2. Navigates to a specific product page using the provided product name.
        3. Validates that the displayed product name matches the expected product name.
        4. Adds the product to the cart and verifies the cart icon count.
        5. Navigates to the cart to check the products listed there.
        6. Verifies that the expected product is present in the cart.
        7. Confirms that the product is not available for addition (removal button should be present).
        8. Resets the application state after the test to ensure a clean environment for future tests.
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

            # Click on the product to view its details
            single_product_page = products_page.click_product_by_name(product_name)

            # Extract the name of the product displayed on the single product page
            extracted_product_name = single_product_page.get_product_name()
            assert extracted_product_name == product_name, \
                f"Expected product name '{product_name}', but found '{extracted_product_name}'"
            log.info(f"Product name displayed matches expected: {product_name}")

            # Add the product to the cart
            single_product_page.add_product_to_cart()
            log.info(f"Added {product_name} to the cart")

            # Verify that the cart icon count reflects the addition of one product
            cart_icon_count = products_page.get_number_of_products_from_cart_icon()
            assert cart_icon_count == 1, \
                f"Expected cart icon count to be 1, but found {cart_icon_count}"
            log.info("Product count in cart icon verified")

            # Navigate to the cart and retrieve the list of products
            cart_page = products_page.click_shopping_cart()
            products_in_cart = cart_page.get_page_products_name()  # Using pop here is not best practice
            log.info(f"Products in cart: {products_in_cart}")

            # Assert that the product in the cart matches the expected product name
            assert product_name in products_in_cart, \
                f"Expected product '{product_name}' in cart, but found: {products_in_cart}"
            log.info("Product successfully verified in cart")

            # Check if the product can be added again by verifying the presence of the remove button
            products_page = cart_page.continue_shopping()
            assert products_page.check_if_product_added(product_name), \
                f"Product '{product_name}' should be added but not verified on the product page"
            log.info("Product addition verified from the product page")

            # Reset the application state (clean up)
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise
