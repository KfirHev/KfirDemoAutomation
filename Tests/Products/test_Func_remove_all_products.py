import time
import pytest
from PageObjects.HomePage import HomePage
from Utils.BaseClass import BaseClass


#@pytest.mark.skip
class TestProductsPageRemove(BaseClass):
    """Tests for the Products Page remove functionality."""

    def test_remove_products_from_cart(self):
        """
        Test the functionality of removing all products from the cart and verifying
        that the cart is empty. The test performs the following actions:

        1. Logs into the application.
        2. Adds all products on the page to the cart.
        3. Removes all products from the cart.
        4. Verifies that no products remain in the cart.
        5. Resets the application state to ensure a clean environment for future tests.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Add all products on the page
            products_page.add_all_products_to_cart()
            log.info("Added all page's products to the cart")

            # Remove all products from the cart
            products_page.remove_all_products_from_the_cart()
            log.info("Removed all page's products from the cart")

            # Verify that all products have been removed
            cart_icon_count = products_page.get_number_of_products_from_cart_icon()
            assert cart_icon_count == 0, \
                f"Expected no products, but found {cart_icon_count} on the cart icon"
            log.info(f"Number of products on the cart icon is '{cart_icon_count}'")

            # Add all products on the page again
            products_page.add_all_products_to_cart()
            log.info("Added all page's products to the cart")

            # Navigate to the shopping cart and retrieve the products listed there
            cart_page = products_page.click_shopping_cart()

            # Remove all products from the cart
            cart_page.remove_all_products_from_the_cart()
            log.info("Removed all products from the cart")

            # Verify again that all products have been removed
            cart_icon_count = products_page.get_number_of_products_from_cart_icon()
            assert cart_icon_count == 0, \
                f"Expected no products, but found {cart_icon_count} on the cart icon"
            log.info(f"Number of products on the cart icon is '{cart_icon_count}'")

            # Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise
