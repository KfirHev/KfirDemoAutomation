from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from PageObjects.CheckOutPage import CheckOutPage
from Utils.BaseClass import BaseClass


class HomePage(BaseClass):

    def __init__(self, driver):
        self._driver = driver

    l_shop = (By.CSS_SELECTOR, "a[href*='shop']")
    l_user_name = (By.CSS_SELECTOR, "input[name='name']")
    l_email = (By.CSS_SELECTOR, "input[name='email']")
    l_password = (By.ID, 'exampleInputPassword1')
    l_ice_cream = (By.ID, 'exampleCheck1')
    l_gender = (By.ID, 'exampleFormControlSelect1')
    l_employ_stat = ((By.XPATH, "//input[@value='option1']"), (By.XPATH, "//input[@value='option2']"))
    l_submit = (By.XPATH, "//input[@type='submit']")
    l_success = (By.CSS_SELECTOR, '.alert-success')

    def shop_items(self):
        self._driver.find_element(*HomePage.l_shop).click()  # deserialize shop tuple
        check_out_page = CheckOutPage(self._driver)
        return check_out_page

    def get_name(self) -> WebElement:
        return self._driver.find_element(*HomePage.l_user_name)

    def get_email(self) -> WebElement:
        return self._driver.find_element(*HomePage.l_email)

    def get_pw(self) -> WebElement:
        return self._driver.find_element(*HomePage.l_password)

    def check_ice_cream(self) -> WebElement:
        return self._driver.find_element(*HomePage.l_ice_cream)

    def select_gender(self, gender: str):
        self.select_from_dropdown(HomePage.l_gender, gender)

    def set_employ_stat(self, status: str) -> WebElement:
        try:
            if status.lower() == 'student':
                return self._driver.find_element(*HomePage.l_employ_stat[0])
            elif status.lower() == 'employed':
                return self._driver.find_element(*HomePage.l_employ_stat[1])
            else:
                raise ValueError(f'Unknown status: {status}')
        except NoSuchElementException as e:
            raise NoSuchElementException(f'Element not found for status {status}') from e

    def submit(self) -> WebElement:
        return self._driver.find_element(*HomePage.l_submit)

    def get_success(self) -> WebElement:
        return self._driver.find_element(*HomePage.l_success)
