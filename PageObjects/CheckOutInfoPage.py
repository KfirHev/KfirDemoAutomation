import time

from selenium.webdriver.common.by import By
from PageObjects.CheckOverviewPage import CheckoutOverviewPage
from Utils.BaseClass import BaseClass


class CheckOutInfoPage(BaseClass):
    """Page object model for the Checkout Info Page."""

    # Locators for input fields and the continue button
    l_first_name = (By.ID, "first-name")
    l_last_name = (By.ID, "last-name")
    l_postal_code = (By.ID, "postal-code")
    l_continue = (By.ID, "continue")
    l_err_msg = (By.CSS_SELECTOR, 'h3')
    l_err_msg_btn = (By.CSS_SELECTOR, 'h3 button')

    def __init__(self, driver):
        """
        Initialize the CheckOutInfoPage object.

        :param driver: WebDriver instance for interacting with the page.
        """
        super().__init__()
        self._driver = driver

    def submit_info(self, first_name='Lara', last_name='Croft', postal='US50203040'):
        """
        Fill in the checkout information form and submit it to proceed to the Checkout Overview Page.

        :param first_name: The first name to be entered in the form. Defaults to 'Lara'.
        :param last_name: The last name to be entered in the form. Defaults to 'Croft'.
        :param postal: The postal code to be entered in the form. Defaults to 'US50203040'.

        :return: Returns an instance of the CheckoutOverviewPage.
        """
        # Clear all and fill in first name
        self.clear_first_name()
        if first_name != '':
            self._driver.find_element(*CheckOutInfoPage.l_first_name).send_keys(first_name)

        # Clear and fill in last name
        self.clear_last_name()
        if last_name != '':
            self._driver.find_element(*CheckOutInfoPage.l_last_name).send_keys(last_name)

        # Clear and fill in postal code
        self.clear_postal_code()
        if postal != '':
            self._driver.find_element(*CheckOutInfoPage.l_postal_code).send_keys(postal)

        # Click 'Continue' to proceed
        self._driver.find_element(*CheckOutInfoPage.l_continue).click()

        return CheckoutOverviewPage(self._driver)

    def clear_first_name(self):
        """Clear the first name input field."""
        return self._driver.find_element(*CheckOutInfoPage.l_first_name).clear()

    def clear_last_name(self):
        """Clear the last name input field."""
        self._driver.find_element(*CheckOutInfoPage.l_last_name).clear()

    def clear_postal_code(self):
        """Clear the postal code input field."""
        self._driver.find_element(*CheckOutInfoPage.l_postal_code).clear()

    def get_submit_error_message(self):
        """
        Fetches the error message displayed after a failed submit attempt.

        :return: The login error message as a string.
        """
        return self._driver.find_element(*CheckOutInfoPage.l_err_msg).text

    def clear_submit_error_message(self):
        """
        Clears the submit error message by clicking the error button (usually an 'X' button).

        :return: None
        """
        self._driver.find_element(*CheckOutInfoPage.l_err_msg_btn).click()



