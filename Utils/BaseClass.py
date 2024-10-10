import inspect
import os
import logging
from logging.handlers import RotatingFileHandler
import pytest
import selenium.webdriver.support.expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException


@pytest.mark.usefixtures('setup_browser')
class BaseClass:
    """Base class for test automation framework providing common utility methods."""

    # Locators
    l_side_menu_button = (By.ID, "react-burger-menu-btn")
    l_shop_cart = (By.CLASS_NAME, "shopping_cart_link")
    l_cart_icon_number_of_products = (By.CSS_SELECTOR, ".shopping_cart_badge")
    l_title = (By.CSS_SELECTOR, ".title")

    # 1. Logging utility
    @staticmethod
    def get_logger() -> logging.Logger:
        """Set up and return a logger instance.

        :return: Configured logger instance.
        """
        logger_name = inspect.stack()[1][3]  # Set logger name to the calling method's name
        logger = logging.getLogger(logger_name)

        # Clear existing handlers to avoid duplicate logs
        if logger.hasHandlers():
            logger.handlers.clear()

        # Ensure the Logs directory exists
        os.makedirs('Logs', exist_ok=True)

        # Define the file handler for rotating logs
        file_handler = RotatingFileHandler(
            'Logs/logfile.log',  # Log file location
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5  # Keep up to 5 backup files
        )
        # Define the log format
        formatter = logging.Formatter('%(asctime)s :%(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    # 2. Product-specific methods
    def get_page_title(self):

        title = self._driver.find_element(*self.l_title).text
        return title

    def get_number_of_products_from_cart_icon(self) -> int:
        """Returns the number of products displayed in the cart icon.

        :return: The product count as an int.
        """
        try:
            products_count = self._driver.find_element(*self.l_cart_icon_number_of_products)
            if products_count.is_displayed():
                return int(products_count.text)
        except NoSuchElementException:
            pass
        return 0

    def click_shopping_cart(self):
        """Navigates to the shopping cart by clicking the cart icon.

        :return: CartPage object representing the cart page.
        """
        from PageObjects.CartPage import CartPage  # Lazy import
        self._driver.find_element(*self.l_shop_cart).click()
        return CartPage(self._driver)

    def get_products_name(self, locator):
        """Fetches the name(s) of products on the page.

        :param locator: Locator for the products.
        :return: The name of a single product if there's only one, or a list of product names if there are multiple.
        """
        products = self._driver.find_elements(*locator)
        products_name = [p.text for p in products]

        if len(products_name) == 1:  # Return a single product name if there's only one product
            return products_name[0]

        return products_name

    def log_out(self):
        """
        Logs out of the application using the sidebar's log out method.

        This method first verifies the side menu button is displayed, then
        clicks the button to open the menu and logs out via the Sidebar object.

        :return: HomePage object representing the user being redirected to the home page.
        """
        # Verify the side menu button is visible before proceeding
        self.verify_element_displayed(self.l_side_menu_button)

        # Open the sidebar by clicking the side menu button
        self._driver.find_element(*self.l_side_menu_button).click()

        # Perform the logout using the sidebar
        from PageObjects.SideBar import SideBar
        if not hasattr(self, '_sidebar'):  # Todo see if needed
            self._sidebar = SideBar(self._driver)
            self._sidebar.log_out()

        # Redirect back to the home page after logging out
        from PageObjects.HomePage import HomePage
        return HomePage(self._driver)

    def reset_application_state(self):
        """
        Resets the application state through the sidebar.

        This method opens the sidebar and calls the reset function from the Sidebar class to clear the session.

        :param _sidebar: Sidebar object used to reset the application state and log out.
        """
        self._driver.find_element(*self.l_side_menu_button).click()
        from PageObjects.SideBar import SideBar
        self._sidebar = SideBar(self._driver)
        self._sidebar.reset_app_and_logout()

    # 3. General helper methods

    def verify_link_clickable(self, locator) -> bool:
        """Verify if a link is clickable.

        :param locator: Locator for the link.
        :return: True if clickable, False otherwise.
        """
        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def verify_element_displayed(self, locator) -> bool:
        """Verify if an element is displayed on the page.

        :param locator: Locator for the element.
        :return: True if displayed, False otherwise.
        """
        try:
            WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def select_from_dropdown(self, locator, value) -> None:
        """Select a value from a dropdown menu.

        :param locator: Locator for the dropdown.
        :param value: The visible text of the option to select.
        :raises NoSuchElementException: If the provided value is not found in the dropdown.
        """
        dropdown = Select(self._driver.find_element(*locator))
        try:
            dropdown.select_by_visible_text(value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f'Unknown value: {value}') from e
