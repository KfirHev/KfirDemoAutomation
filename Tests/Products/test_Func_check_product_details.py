import pytest
import allure
from PageObjects.HomePage import HomePage
from TestData.SingleProductPageData import SingleProductPageData
from Utils.BaseClass import BaseClass


# @pytest.mark.skip
@allure.feature("Product details")
@allure.story("Product details Discrepancy Check")
@allure.severity(allure.severity_level.CRITICAL)
class TestCheckProductDetails(BaseClass):
    """
    Tests for verifying product details and add-to-cart functionality on the Products Page.

    Steps:
    1. Log into the application and navigate to the Products Page.
    2. Add the product specified in the test data to the cart.
    3. Capture the product's details, price, and image from the Products Page.
    4. Navigate to the Single Product Page by clicking the product name.
    5. Verify that product details, price, and image match between both pages.
    6. Reset the application state at the end of the test.
    """

    @pytest.fixture(params=SingleProductPageData.test_single_product)
    def get_data(self, request):
        """
        Pytest fixture to get data for products tests.

        :param request: Data parameter for the test method.
        :return: Returns parameterized test data for the test.
        """
        return request.param

    def test_check_product_info(self, get_data):
        """
        Test to verify product details on both the Products Page and Single Product Page.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Extract the product name from the test data
            product_name = get_data['product_name']
            log.info(f"Starting test for product: {product_name}")

            # Log into the application
            products_page = home_page.login()
            log.info("Login successful, navigated to Products Page")

            # Add the specified product to the cart
            products_page.add_product_to_cart(product_name)
            log.info(f"Added {product_name} to the cart")

            # Extract product details, price, and image URL from the Products Page
            product_details = products_page.get_product_details(product_name)
            product_price = products_page.get_product_price(product_name)
            product_image = products_page.get_product_image(product_name)

            # Navigate to the Single Product Page by clicking the product name
            single_product_page = products_page.click_product_by_name(product_name)

            # Extract product details from the Single Product Page
            single_product_details = single_product_page.get_product_details()
            single_product_price = single_product_page.get_product_price()
            single_product_image = single_product_page.get_product_image()

            # Verify that product details match
            assert product_details == single_product_details, \
                f"Expected product details to match. Expected: {product_details}, but got: {single_product_details}"
            log.info("Product details match as expected")

            # Verify that product prices match
            assert product_price == single_product_price, \
                f"Expected product price to match. Expected: {product_price}, but got: {single_product_price}"
            log.info("Product price matches as expected")

            # Compare the images of the product
            assert single_product_page.compare_images(product_image, single_product_image), \
                f"Expected product images to match. Compare {single_product_image} with {product_image}"
            log.info("Product image matches as expected")

            # Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An error occurred during the test: {e}")
            raise
