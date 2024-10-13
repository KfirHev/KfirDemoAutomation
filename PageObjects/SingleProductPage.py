import time
from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass


class SingleProductPage(BaseClass):
    """Page object model for the Products Page, handling product interactions and cart management."""

    # Locators for elements on the Products Page
    l_product_name = (By.CSS_SELECTOR, ".inventory_details_name")
    l_product_price = (By.CSS_SELECTOR, ".inventory_details_price")
    l_product_details = (By.CSS_SELECTOR, ".inventory_details_desc")
    l_product_image = (By.CSS_SELECTOR, ".inventory_details_img")
    l_add_to_cart_button = (By.XPATH, "//button[text() = 'Add to cart']")
    l_remove_from_cart_button = (By.XPATH, "//button[text() = 'Remove']")  # Todo move to base class
    l_back_to_products = (By.ID, "back-to-products")

    def __init__(self, driver):
        """
        Initializes the ProductsPage object with the WebDriver instance and a SideBar instance.

        :param driver: WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver

    def get_product_name(self):
        """Retrieve the product name."""
        return self._driver.find_element(*self.l_product_name).text

    def get_product_price(self):
        """Retrieve the product price."""
        return self._driver.find_element(*self.l_product_price).text

    def get_product_details(self):
        """Retrieve the product description."""
        return self._driver.find_element(*self.l_product_details).text

    def get_product_image(self):
        """Retrieve the product image URL."""
        return self._driver.find_element(*self.l_product_image).get_attribute('src')

    def add_product_to_cart(self):
        """Add the product to the cart."""
        self._driver.find_element(*self.l_add_to_cart_button).click()

    def remove_product_from_cart(self):
        """Remove the product from the cart."""
        self._driver.find_element(*self.l_remove_from_cart_button).click()

    def back_to_product_page_click(self):
        """
        Navigate back to the products page.

        :return: ProductsPage instance.
        """
        self._driver.find_element(*self.l_back_to_products).click()
        from PageObjects.ProductsPage import ProductsPage
        return ProductsPage(self._driver)
