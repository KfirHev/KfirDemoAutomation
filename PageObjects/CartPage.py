from selenium.webdriver.common.by import By
from PageObjects.SideBar import SideBar
from Utils.BaseClass import BaseClass


class CartPage(BaseClass):
    """Page object model for the Cart Page."""

    # Locators for elements on the Cart Page
    l_all_page_products_names = (By.CSS_SELECTOR, ".inventory_item_name")
    l_continue_shopping_button = (By.ID, "continue-shopping")
    l_remove_from_cart_buttons = (By.XPATH, "//button[text() = 'Remove']")

    def __init__(self, driver):
        """
        Initializes the CartPage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        super().__init__()
        self._driver = driver

    def get_page_products_name(self):
        """
        Retrieves the names of all products displayed on the cart page.

        :return: A list of product names on the cart page.
        """
        # Using BaseClass method
        return self.get_products_name(CartPage.l_all_page_products_names)

    def continue_shopping(self):
        self._driver.find_element(*CartPage.l_continue_shopping_button).click()
        from PageObjects.ProductsPage import ProductsPage
        return ProductsPage(self._driver)

    def remove_all_products_from_the_cart(self):  # TODO move locator and method to base class ? count usage
        """
        Removes all visible products from the cart by clicking on each "Remove" button.
        """
        remove_from_cart_buttons = self._driver.find_elements(*CartPage.l_remove_from_cart_buttons)
        for button in remove_from_cart_buttons:
            button.click()




