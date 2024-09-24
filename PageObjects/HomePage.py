from Utils.BaseClass import BaseClass
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from PageObjects.ProductsPage import ProductsPage


# Todo catch exceptions in BaseClass ?

class HomePage(BaseClass):
    """Page object model for the Home Page."""

    # Locators for elements on the Home Page
    l_logo = (By.CSS_SELECTOR, ".login_logo")
    l_user_name = (By.ID, 'user-name')
    l_pw = (By.ID, 'password')
    l_login_btn = (By.ID, 'login-button')
    l_valid_users = (By.ID, 'login_credentials')
    l_valid_pw = (By.CSS_SELECTOR, '.login_password')

    def __init__(self, driver):
        """
        Initializes the HomePage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        self._driver = driver

    def get_title(self) -> str:
        """
        Fetches the page title.

        :return: The title of the current page.
        """
        return self._driver.title

    def is_logo_displayed(self) -> bool:
        """
        Verifies if the logo is displayed on the page.

        :return: True if the logo is displayed, False otherwise.
        """
        try:
            return self._driver.find_element(*HomePage.l_logo).is_displayed()
        except NoSuchElementException:
            return False

    def is_login_btn_displayed(self) -> bool:
        """
        Verifies if the login button is displayed on the page.

        :return: True if the login button is displayed, False otherwise.
        """
        try:
            return self._driver.find_element(*HomePage.l_login_btn).is_displayed()
        except NoSuchElementException:
            return False

    def get_valid_user_name(self) -> list:
        """
        Extracts the list of valid usernames from the page.

        :return: List of valid usernames found in the 'login_credentials' div.
        """
        try:
            user_div = self._driver.find_element(*HomePage.l_valid_users)

            # Split inner HTML by <br> tags to separate usernames
            usernames = user_div.get_attribute('innerHTML').split('<br>')

            # Extract the first username (after the 'Accepted usernames' header)
            first_username = usernames[0].split('>')[-1]

            # Strip whitespace and filter out empty usernames
            return [first_username] + [username.strip() for username in usernames[1:] if username.strip()]
        except NoSuchElementException:
            return []  # Return an empty list if the element is not found

    def get_password(self) -> str:
        """
        Extracts the password from the login password div.

        :return: The password found after the h4 tag.
        """
        try:
            # Find the password div
            password_div = self._driver.find_element(*HomePage.l_valid_pw)

            # Get the inner text of the div
            full_text = password_div.get_attribute('innerHTML')

            # Split the text by the closing h4 tag and strip any excess whitespace
            password = full_text.split('</h4>')[-1].strip()

            return password
        except NoSuchElementException:
            return ""  # Return an empty string if the password div is not found

    def get_user_hint(self):
        return self._driver.find_element(*self.l_user_name).get_attribute('placeholder')

    def get_password_hint(self):
        return self._driver.find_element(*self.l_pw).get_attribute('placeholder')

    def login(self, user, pw):

        """
        Locate and return the login button on the home page.

        :return: WebElement representing the login button.
        """
        self._driver.find_element(*HomePage.l_user_name).send_keys(user)
        self._driver.find_element(*HomePage.l_pw).send_keys(pw)
        self._driver.find_element(*HomePage.l_login_btn).click()
        return ProductsPage(self._driver)
