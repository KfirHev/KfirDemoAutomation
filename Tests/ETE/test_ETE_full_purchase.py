import time
import pytest
from PageObjects.HomePage import HomePage
from Utils.BaseClass import BaseClass


class TestFullPurchase(BaseClass):
    """
    Test class for performing a full purchase flow, from login to final purchase confirmation.
    """

    def test_complete_purchase(self):
        """
        Test complete purchase flow:
        - Step 1: Log into the application.
        - Step 2: Add a specified product to the cart.
        - Step 3: Proceed to checkout and submit user information.
        - Step 4: Verify the final total price (subtotal + tax).
        - Step 5: Complete the purchase and check for success message.
        - Step 6: Reset the application state.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Step 1: Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Step 2: Add the product to the cart
            products_page.add_product_to_cart('Sauce Labs Onesie')
            cart_page = products_page.click_shopping_cart()

            # Step 3: Proceed to checkout and submit user information
            checkout_info_page = cart_page.checkout()
            check_out_overview_page = checkout_info_page.submit_info()

            # Step 4: Verify that the total price (subtotal + tax) is correct
            assert check_out_overview_page.check_total_price(), \
                "Total price calculation is incorrect."
            log.info("Total price calculation (including tax) is correct")

            # Step 5: Complete the purchase and verify success message
            check_out_complete = check_out_overview_page.finish_buy()
            success_message = check_out_complete.get_success_message()
            assert success_message == 'Thank you for your order!', \
                f"Purchase was unsuccessful. Expected 'Thank you for your order!', but got '{success_message}'"
            log.info("Purchase was completed successfully")

            # Step 6: Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
