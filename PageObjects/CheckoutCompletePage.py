from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass


class CheckoutCompletePage(BaseClass):
    # Locators for elements on the CheckoutOverView Page

    #l_cart_items = (By.CSS_SELECTOR, '.cart_item')


    def __init__(self, driver):
        """
        Initializes the CartPage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        super().__init__()
        self._driver = driver
