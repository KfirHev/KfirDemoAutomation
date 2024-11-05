import pytest
from PageObjects.HomePage import HomePage
from Utils.BaseClass import BaseClass


class TestSubmitData(BaseClass):
    """
    Test class for submitting checkout information.

    Test Steps:
    1. Log into the application.
    2. Add all products to the cart and navigate to the shopping cart.
    3. Proceed to the checkout page.
    4. Submit default checkout info (first name: 'Lara', last name: 'Croft', postal: 'US50203040').
    5. Verify successful submission by checking the page title is 'Checkout: Overview'.
    6. Reset application state to avoid side effects on other tests.
    """

    def test_submit_info(self):

        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Add all products to the cart and navigate to checkout
            products_page.add_all_products_to_cart()
            cart_page = products_page.click_shopping_cart()
            checkout_info_page = cart_page.checkout()

            # Submit default checkout info (first name: 'Lara', last name: 'Croft', postal: 'US50203040')
            check_out_overview_page = checkout_info_page.submit_info()
            overview_page_title = check_out_overview_page.get_page_title()

            # Verify the submission was successful
            assert overview_page_title == 'Checkout: Overview', \
                f"Checkout info submission was unsuccessful. Expected 'Checkout: Overview', but got '{overview_page_title}'"
            log.info("Checkout info submitted and verified successfully")

            # Reset the application state to avoid side effects on other tests
            check_out_overview_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise  # Re-raise any other exception to fail the test


