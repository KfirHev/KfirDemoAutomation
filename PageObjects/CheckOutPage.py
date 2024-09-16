from selenium.webdriver.common.by import By
from PageObjects.ConfirmPage import ConfirmPage


class CheckOutPage:

    def __init__(self, driver):
        self._driver = driver

    # self.driver.find_element(By.CSS_SELECTOR, "app-card:nth-child(4) button").click()
    # self.driver.find_element(By.CSS_SELECTOR, ".nav-item.active").click()

    select_product = (By.CSS_SELECTOR, "app-card:nth-child(4) button")
    checkout = (By.CSS_SELECTOR, ".nav-item.active")

    def select_products(self):
        return self._driver.find_element(*CheckOutPage.select_product)

    def checkout_products(self):
        self._driver.find_element(*CheckOutPage.checkout).click()
        confirm_products = ConfirmPage(self._driver)
        return confirm_products
