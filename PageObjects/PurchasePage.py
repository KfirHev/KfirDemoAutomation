from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from Utils.BaseClass import BaseClass


class PurchasePage(BaseClass):

    def __init__(self, driver):
        self._driver = driver

    search_country = (By.CSS_SELECTOR, " #country")
    select_country = (By.XPATH, "//a[contains(text(),'India')]")
    wait_country = (By.LINK_TEXT, 'India')
    check_conditions = (By.CSS_SELECTOR, ".checkbox")
    purchase = (By.XPATH, "// input[@value = 'Purchase']")
    wait_msg = (By.CSS_SELECTOR, ".alert")

    def locate_country(self) -> WebElement:  # Adding explicit type for pycharm to understand return type
        return self._driver.find_element(*PurchasePage.search_country)

    def get_country(self) -> WebElement:
        # self._wait.until(EC.element_to_be_clickable(PurchasePage.wait_country))  # MOVED TO BASE CLASS UTILS
        self.verify_link_clickable(PurchasePage.wait_country)
        return self._driver.find_element(*PurchasePage.select_country)

    def sign_conditions(self) -> WebElement:
        return self._driver.find_element(*PurchasePage.check_conditions)

    def fin_purchase(self) -> WebElement:
        return self._driver.find_element(*PurchasePage.purchase)

    def get_success(self) -> WebElement:
        # self._wait.until(EC.presence_of_element_located(PurchasePage.wait_msg)) # MOVED TO BASE CLASS UTILS
        self.verify_link_presence(PurchasePage.wait_msg)
        return self._driver.find_element(*PurchasePage.wait_msg)
