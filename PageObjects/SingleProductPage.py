import time
from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass
from PageObjects.SideBar import SideBar


class SingleProductPage(BaseClass):
    """Page object model for the Products Page, handling product interactions and cart management."""

    # Locators for elements on the Products Page
    l_product_name = (By.CSS_SELECTOR, ".inventory_details_name")
    l_add_to_cart_button = (By.XPATH, "//button[text() = 'Add to cart']")
    l_remove_from_cart_button = (By.XPATH, "//button[text() = 'Remove']") # Todo move to base class
    l_back_to_products = (By.ID, "back-to-products")
    l_product_price = (By.CSS_SELECTOR, ".inventory_details_price")

    def __init__(self, driver):
        """
        Initializes the ProductsPage object with the WebDriver instance and a SideBar instance.

        :param driver: WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver

        # Initialize Sidebar for sidebar actions
        self._sidebar = SideBar(self._driver)

    def get_product_name(self):
        return self._driver.find_element(*SingleProductPage.l_product_name).text

    def get_product_price(self):
        return self._driver.find_element(*SingleProductPage.l_product_price).text

    def add_product_to_cart(self):
        self._driver.find_element(*SingleProductPage.l_add_to_cart_button).click()

    def remove_product_from_cart(self):
        self._driver.find_element(*SingleProductPage.l_remove_from_cart_button).click()

    def back_to_product_page_click(self):
        self._driver.find_element(*SingleProductPage.l_back_to_products).click()
        from PageObjects.ProductsPage import ProductsPage
        return ProductsPage(self._driver)
