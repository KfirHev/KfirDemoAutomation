import time
from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass
from PageObjects.CartPage import CartPage
from PageObjects.SideBar import SideBar


class SingleProductPage(BaseClass):
    """Page object model for the Products Page, handling product interactions and cart management."""

    # Locators for elements on the Products Page
    l_side_menu_button = (By.ID, "react-burger-menu-btn")
    l_product_name = (By.CSS_SELECTOR, ".inventory_details_name")
    l_add_to_cart_button = (By.XPATH, "//button[text() = 'Add to cart']")
    # l_shop_cart = (By.CLASS_NAME, "shopping_cart_link") # moved to base class
    # l_cart_icon_number_of_products = (By.CSS_SELECTOR, ".shopping_cart_badge") # moved to base class

    def __init__(self, driver):
        """
        Initializes the ProductsPage object with the WebDriver instance and a SideBar instance.

        :param driver: WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver

        # Initialize Sidebar for sidebar actions
        self._sidebar = SideBar(self._driver)
