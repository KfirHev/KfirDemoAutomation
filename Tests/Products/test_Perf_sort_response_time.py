import time
import pytest
import allure
from PageObjects.HomePage import HomePage
from TestData.ProductPageData import ProductPageData
from Utils.BaseClass import BaseClass


@pytest.mark.xfail
@allure.feature("Product Sorting")
@allure.story("Sorting Response Time Check")
@allure.severity(allure.severity_level.CRITICAL)
class TestProductPageSortPerformance(BaseClass):
    """
    Tests the performance of product sorting functionality by measuring response times.
    """

    MAX_RESPONSE_TIME = 5  # Maximum allowable response time (in seconds) for sorting actions.

    @pytest.fixture(params=ProductPageData.test_sorting_options)
    def get_data(self, request):
        """
        Pytest fixture to provide sorting options for each test case.

        :param request: The request object containing parameterized test data.
        :return: A dictionary with the sorting option to be tested.
        """
        return request.param

    def test_sorting_response_time(self, get_data):
        """
        Measures the response time for sorting products and checks it against a maximum threshold.

        :param get_data: A dictionary containing the sorting option to be tested.
        """
        log = self.get_logger()
        home_page = HomePage(self.driver)
        products_page = None

        try:
            sort_option = get_data['option_name']
            log.info(f"Starting test with sorting option: {sort_option}")

            products_page = home_page.login(user='performance_glitch_user')
            log.info("Login successful")

            start_time = time.time()
            products_page.sort_products_by(sort_option)
            end_time = time.time()

            sort_response_time = round((end_time - start_time), 3)
            log.info(f"Sorting response time for option '{sort_option}': {sort_response_time} seconds")

            assert sort_response_time <= self.MAX_RESPONSE_TIME, (
                f"Sorting response time exceeded {self.MAX_RESPONSE_TIME} "
                f"seconds for sorting option '{sort_option}': {sort_response_time} seconds."
            )

        except AssertionError as ae:
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            log.error(f"An unexpected error occurred during the test: {e}")
            raise

        finally:
            if products_page:
                products_page.reset_application_state()
                log.info("Application state reset successful")
