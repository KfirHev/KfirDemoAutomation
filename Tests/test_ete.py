import pytest
from Utils.BaseClass import BaseClass
from PageObjects.HomePage import HomePage
from PageObjects.CheckOutPage import CheckOutPage
from PageObjects.ConfirmPage import ConfirmPage
from PageObjects.PurchasePage import PurchasePage


# @pytest.mark.usefixtures('setup_browser')  == placed in BaseClass
class TestOne(BaseClass):

    def test_e2e(self):
        # driver.find_element(By.XPATH, "//a[@href='/angularpractice/shop']").click()
        log = self.get_logger()
        home_page = HomePage(self.driver)
        check_out_page = home_page.shop_items()

        # # NEED TO REPLACE WITH CHAINING METHOD
        # self.driver.find_element(By.CSS_SELECTOR, "app-card:nth-child(4) button").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".nav-item.active").click()
        # check_out_page = CheckOutPage(self.driver)
        check_out_page.select_products().click()
        confirm_products = check_out_page.checkout_products()

        # self.driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        # confirm_products = ConfirmPage(self.driver)

        purchase_products = confirm_products.confirm_products()

        # self.driver.find_element(By.CSS_SELECTOR, " #country").send_keys('india')
        # self.driver.find_element(By.XPATH, "//a[contains(text(),'India')]").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".checkbox").click()
        # self.driver.find_element(By.XPATH, "// input[@value = 'Purchase']").click()
        # wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert")))
        # msg = self.driver.find_element(By.CSS_SELECTOR, ".alert").text
        # purchase_products = PurchasePage(self.driver)

        purchase_products.locate_country().send_keys('india')
        log.info(f'country sent to application is india')
        purchase_products.get_country().click()
        purchase_products.sign_conditions().click()
        purchase_products.fin_purchase().click()
        msg = purchase_products.get_success().text
        log.info(f'text message received from application is {msg}')

        assert 'Success' in msg
