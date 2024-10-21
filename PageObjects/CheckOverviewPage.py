from selenium.webdriver.common.by import By
from PageObjects.CheckoutCompletePage import CheckoutCompletePage
from Utils.BaseClass import BaseClass


class CheckoutOverviewPage(BaseClass):
    # Locators for elements on the CheckoutOverview Page
    l_cart_items = (By.CSS_SELECTOR, '.cart_item')
    l_subtotal_price = (By.CSS_SELECTOR, '.summary_subtotal_label')
    l_tax = (By.CSS_SELECTOR, '.summary_tax_label')
    l_total_price = (By.CSS_SELECTOR, '.summary_total_label')
    l_finish = (By.XPATH, "//button[text() = 'Finish']")

    # Constant for tax rate
    TAX_RATE = 0.08

    def __init__(self, driver):
        """
        Initializes the CheckoutOverviewPage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        super().__init__()
        self._driver = driver

    def _get_subtotal_price(self):
        """
        Retrieves the subtotal price from the page.

        :return: Subtotal price as a float.
        """
        # The first 13 characters represent the label (e.g., "Item total: "), so we slice them off
        return float(self._driver.find_element(*self.l_subtotal_price).text[13:])

    def _get_tax(self):
        """
        Retrieves the tax amount from the page.

        :return: Tax amount as a float.
        """
        # The first 6 characters represent the label (e.g., "Tax: "), so we slice them off
        return float(self._driver.find_element(*self.l_tax).text[6:])

    def _get_total_price(self):
        """
        Retrieves the total price from the page.

        :return: Total price as a float.
        """
        # The first 8 characters represent the label (e.g., "Total: "), so we slice them off
        return float(self._driver.find_element(*self.l_total_price).text[8:])

    def check_sub_total_price(self):
        """
        Compares the calculated subtotal based on the cart items with the displayed subtotal on the page.

        :return: True if the calculated subtotal matches the displayed subtotal, False otherwise.
        """
        calc_subtotal = 0
        displayed_subtotal = self._get_subtotal_price()

        # Iterate through each product in the cart and sum up the prices
        products = self._driver.find_elements(*self.l_cart_items)
        for product in products:
            product_price = float(product.find_element(By.CSS_SELECTOR, '.inventory_item_price').text.strip('$'))
            calc_subtotal += product_price

        # Round the calculated subtotal to 2 decimal places
        calc_subtotal = round(calc_subtotal, 2)

        return calc_subtotal == displayed_subtotal

    def check_tax(self):
        """
        Compares the calculated tax based on the subtotal with the displayed tax on the page.

        :return: True if the calculated tax matches the displayed tax, False otherwise.
        """
        displayed_tax = round(self._get_tax(), 2)

        # Calculate the expected tax using the subtotal and the tax rate
        calc_tax = round(self._get_subtotal_price() * self.TAX_RATE, 2)

        return calc_tax == displayed_tax

    def check_total_price(self):
        """
        Compares the calculated total price (subtotal + tax) with the displayed total price on the page.

        :return: True if the calculated total matches the displayed total, False otherwise.
        """
        displayed_total_price = self._get_total_price()
        subtotal = self._get_subtotal_price()
        tax = self._get_tax()

        # Calculate the total price by summing the subtotal and tax
        calc_total_price = round(subtotal + tax, 2)

        return calc_total_price == displayed_total_price

    def finish_buy(self):
        """
        Completes the checkout process by clicking the 'Finish' button.

        :return: A CheckoutCompletePage object after the checkout is completed.
        """
        self._driver.find_element(*self.l_finish).click()
        return CheckoutCompletePage(self._driver)
