from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass


class CheckoutCompletePage(BaseClass):
    # Locators for elements on the CheckoutOverView Page

    l_success_msg = (By.TAG_NAME, 'h2')

    def __init__(self, driver):
        """
        Initializes the CheckoutCompletePage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        super().__init__()
        self._driver = driver

    def get_success_message(self):
        """
        Fetches the error message displayed after a failed submit attempt.

        :return: The login error message as a string.
        """
        return self._driver.find_element(*CheckoutCompletePage.l_success_msg).text
