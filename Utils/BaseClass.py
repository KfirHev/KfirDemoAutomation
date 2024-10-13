import inspect
import os
import logging
from logging.handlers import RotatingFileHandler
import pytest
import requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, TimeoutException


@pytest.mark.usefixtures('setup_browser')
class BaseClass:
    """Base class for the test automation framework, providing common utility methods."""

    # Locators for common elements across pages
    l_side_menu_button = (By.ID, "react-burger-menu-btn")
    l_shop_cart = (By.CLASS_NAME, "shopping_cart_link")
    l_cart_icon_number_of_products = (By.CSS_SELECTOR, ".shopping_cart_badge")
    l_title = (By.CSS_SELECTOR, ".title")

    # 1. Logging utility
    @staticmethod
    def get_logger() -> logging.Logger:
        """Sets up and returns a logger instance.

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
    def get_page_title(self) -> str:
        """Retrieve the page title text."""
        title = self._driver.find_element(*self.l_title).text
        return title

    def get_number_of_products_from_cart_icon(self) -> int:
        """Returns the number of products displayed in the cart icon.

        :return: The product count as an int, or 0 if none are found.
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
        from PageObjects.CartPage import CartPage  # Lazy import to avoid circular dependencies
        self._driver.find_element(*self.l_shop_cart).click()
        return CartPage(self._driver)

    def get_products_name(self, locator):
        """Fetches the name(s) of products on the page.

        :param locator: Locator for the products.
        :return: The name of a single product if there's only one, or a list of product names if there are multiple.
        """
        products = self._driver.find_elements(*locator)
        products_name = [p.text for p in products]

        if len(products_name) == 1:
            return products_name[0]

        return products_name

    def log_out(self):
        """Logs out of the application using the sidebar's log out method.

        Verifies the side menu button is displayed, clicks it to open the menu, and logs out.

        :return: HomePage object representing the home page after logging out.
        """
        # Verify the side menu button is visible
        self.verify_element_displayed(self.l_side_menu_button)

        # Open the sidebar by clicking the side menu button
        self._driver.find_element(*self.l_side_menu_button).click()

        # Perform logout via Sidebar
        from PageObjects.SideBar import SideBar
        if not hasattr(self, '_sidebar'):  # Sidebar instance only initialized when needed
            self._sidebar = SideBar(self._driver)
        self._sidebar.log_out()

        # Redirect back to the home page
        from PageObjects.HomePage import HomePage
        return HomePage(self._driver)

    def reset_application_state(self):
        """Resets the application state through the sidebar.

        Opens the sidebar and calls the reset function from the Sidebar class.
        """
        self._driver.find_element(*self.l_side_menu_button).click()
        from PageObjects.SideBar import SideBar
        self._sidebar = SideBar(self._driver)
        self._sidebar.reset_app_and_logout()

    # 3. General helper methods

    @staticmethod
    def compare_images(image1_url: str, image2_url: str) -> bool:
        """Compares two images from their URLs and returns True if they are the same.

        :param image1_url: URL of the first image.
        :param image2_url: URL of the second image.
        :return: True if the images are identical, otherwise False.
        """
        # Download and open the first image
        response1 = requests.get(image1_url)
        response1.raise_for_status()
        img1 = Image.open(BytesIO(response1.content))

        # Download and open the second image
        response2 = requests.get(image2_url)
        response2.raise_for_status()
        img2 = Image.open(BytesIO(response2.content))

        # Resize both images to a common size for comparison
        size = (256, 256)
        img1_resized = img1.resize(size)
        img2_resized = img2.resize(size)

        # Compare the pixel data
        return list(img1_resized.getdata()) == list(img2_resized.getdata())

    def verify_link_clickable(self, locator) -> bool:
        """Verifies if a link is clickable.

        :param locator: Locator for the link.
        :return: True if the link is clickable, False if it times out.
        """
        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    def verify_element_displayed(self, locator) -> bool:
        """Verifies if an element is displayed on the page.

        :param locator: Locator for the element.
        :return: True if the element is displayed, False otherwise.
        """
        try:
            WebDriverWait(self._driver, 10).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def select_from_dropdown(self, locator, value) -> None:
        """Selects a value from a dropdown menu.

        :param locator: Locator for the dropdown.
        :param value: The visible text of the option to select.
        :raises NoSuchElementException: If the provided value is not found in the dropdown.
        """
        dropdown = Select(self._driver.find_element(*locator))
        try:
            dropdown.select_by_visible_text(value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f'Unknown value: {value}') from e
