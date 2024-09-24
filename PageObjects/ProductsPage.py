from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass

# Todo catch exceptions in BaseClass ?
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class ProductsPage(BaseClass):
    """Page object model for the Home Page."""

    # Locators for elements on the Home Page
    l_side_menu_button = (By.ID, "react-burger-menu-btn")
    l_log_out = (By.ID, "logout_sidebar_link")
    l_title = (By.CSS_SELECTOR, ".title")

    def __init__(self, driver):
        """
        Initializes the HomePage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        self._driver = driver

    def log_out(self):

        self.verify_element_displayed(ProductsPage.l_side_menu_button)
        self._driver.find_element(*ProductsPage.l_side_menu_button).click()
        self._driver.find_element(*ProductsPage.l_log_out).click()
        # back to home page
        # Import HomePage here to avoid circular import at the top
        from PageObjects.HomePage import HomePage
        return HomePage(self._driver)

    def get_page_title(self) -> str:
        """
        Fetches the page header title.

        :return: The title of the main header for products page.
        """
        return self._driver.find_element(*ProductsPage.l_title).text

