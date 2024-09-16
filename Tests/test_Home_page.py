import pytest

from PageObjects.HomePage import HomePage
from TestData.HomePageData import HomePageData
from Utils.BaseClass import BaseClass


class TestHomePage(BaseClass):

    def test_form_submit(self, get_data):
        log = self.get_logger()
        home_page = HomePage(self.driver)
        home_page.get_name().send_keys(get_data['first_name'])
        home_page.get_pw().send_keys(get_data['password'])
        home_page.get_email().send_keys(get_data['email'])
        home_page.check_ice_cream().click()
        home_page.select_gender(get_data['gender'])
        home_page.set_employ_stat(get_data['employment_stat']).click()
        home_page.submit().click()
        s_message = home_page.get_success().text
        log.info(f'text message received from application is {s_message}')
        assert 'Success' in s_message
        log.info('Refreshing the browser to clear data')
        self.driver.refresh()  # refreshing the browser to clear data for previous run

    # @pytest.fixture(params=HomePageData.test_home_page_date_submit)  # collect data from module you created
    @pytest.fixture(params=HomePageData.get_data_excel('TestCase2'))
    def get_data(self, request):
        return request.param
