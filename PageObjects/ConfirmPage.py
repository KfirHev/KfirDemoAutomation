from selenium.webdriver.common.by import By
from PageObjects.PurchasePage import PurchasePage


class ConfirmPage:

    def __init__(self, driver):
        self._driver = driver

    # self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()

    confirm = (By.CSS_SELECTOR, ".btn-success")

    def confirm_products(self):
        self._driver.find_element(*ConfirmPage.confirm).click()
        purchase_products = PurchasePage(self._driver)  # for driver set on the next page
        return purchase_products


