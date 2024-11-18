import pytest
import allure
from PageObjects.HomePage import HomePage
from TestData.CheckOutOverviewData import CheckoutOverviewData
from Utils.BaseClass import BaseClass


@allure.feature("Checkout Process")
@allure.story("Calculate Prices In Cart")
@allure.severity(allure.severity_level.CRITICAL)
class TestPriceInCartCalc(BaseClass):
    @pytest.fixture(params=CheckoutOverviewData.test_products)
    def get_data(self, request):
        """
        Fixture to get parameterized test data for verifying prices in the shopping cart.

        This fixture provides product data that includes the product names to add to the cart
        and the expected number of products.

        :param request: Data parameter passed by pytest.
        :return: Returns the test data for the test case.
        """
        return request.param

    def test_prices_in_cart_calculation(self, get_data):
        """
        Test to verify the prices in the shopping cart, including the subtotal, tax, and total price.

        Test steps:
        1. Login to the application.
        2. Add the specified products to the cart.
        3. Verify the number of products added.
        4. Verify that the subtotal is calculated correctly.
        5. Verify that the tax (8%) is calculated correctly.
        6. Verify that the total price is correct (subtotal + tax).
        7. Reset the application state to ensure no side effects for subsequent tests.

        :param get_data: Test data for the current test case (provided by the fixture).
        """
        log = self.get_logger()  # Initialize logger
        home_page = HomePage(self.driver)

        try:
            # Extract necessary data from the test input
            product_name_from_data = get_data['product_names']
            number_of_products_to_add = len(product_name_from_data)

            # Login to the application
            products_page = home_page.login()
            log.info("Login successful")

            # Add specified products to the shopping cart
            log.info(f"Starting test with products: {product_name_from_data}")
            products_page.add_product_to_cart(product_name_from_data)
            log.info(f"Added {product_name_from_data} to the cart")

            # Proceed to the shopping cart and initiate the checkout process

            cart_page = products_page.click_shopping_cart()
            checkout_info_page = cart_page.checkout()

            # Submit default checkout information
            check_out_overview_page = checkout_info_page.submit_info()

            # Verify the number of products in the cart matches the expected count
            assert check_out_overview_page.get_number_of_products_from_cart_icon() == number_of_products_to_add, \
                "The number of products in the cart does not match the expected number."
            log.info("Verified the correct number of products in the cart")

            # Verify that the subtotal is correct
            assert check_out_overview_page.check_sub_total_price(), \
                "Subtotal amount calculation is incorrect."
            log.info("Subtotal amount calculation is correct")

            # Verify that the tax amount is correct (8%)
            assert check_out_overview_page.check_tax(), "Tax amount calculation is incorrect."
            log.info("Tax amount calculation is correct (8%)")

            # Verify that the total price is correct (subtotal + tax)
            assert check_out_overview_page.check_total_price(), \
                "Total price calculation is incorrect."
            log.info("Total price calculation (including tax) is correct")

            # Reset the application state to avoid side effects on other tests
            check_out_overview_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise  # Re-raise the assertion error to mark the test as failed

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise  # Re-raise any unexpected exceptions
