from Utils.BaseClass import BaseClass
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from PageObjects.ProductsPage import ProductsPage


# TODO: Catch exceptions in BaseClass if necessary

class HomePage(BaseClass):
    """Page object model for the Home Page, handling login interactions and element verifications."""

    # Locators for elements on the Home Page
    l_logo = (By.CSS_SELECTOR, ".login_logo")
    l_user_name = (By.ID, 'user-name')
    l_pw = (By.ID, 'password')
    l_login_btn = (By.ID, 'login-button')
    l_valid_users = (By.ID, 'login_credentials')
    l_valid_pw = (By.CSS_SELECTOR, '.login_password')
    l_err_msg = (By.CSS_SELECTOR, 'h3')
    l_err_msg_btn = (By.CSS_SELECTOR, 'h3 button')

    def __init__(self, driver):
        """
        Initializes the HomePage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver

    def get_title(self) -> str:
        """
        Fetches the page title.

        :return: The title of the current page.
        """
        return self._driver.title

    def is_logo_displayed(self) -> bool:
        """
        Verifies if the login logo is displayed on the page.

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
        Extracts the list of valid usernames from the login credentials section.

        :return: A list of valid usernames found in the 'login_credentials' div.
        """
        try:
            user_div = self._driver.find_element(*HomePage.l_valid_users)
            # Split the content by <br> tags to get each username
            usernames = user_div.get_attribute('innerHTML').split('<br>')

            # Extract the first username from the div (skip any preceding headers)
            first_username = usernames[0].split('>')[-1]

            # Clean up the list by stripping whitespace and filtering out empty elements
            return [first_username] + [username.strip() for username in usernames[1:] if username.strip()]
        except NoSuchElementException:
            return []  # Return an empty list if the element is not found

    def get_password(self) -> str:
        """
        Extracts the password from the login password section.

        :return: The valid password provided on the page.
        """
        try:
            # Locate the password div and extract its inner HTML
            password_div = self._driver.find_element(*HomePage.l_valid_pw)
            full_text = password_div.get_attribute('innerHTML')

            # Extract password from the HTML content by splitting after </h4> tag
            password = full_text.split('</h4>')[-1].strip()
            return password
        except NoSuchElementException:
            return ""  # Return an empty string if the password div is not found

    def get_user_hint(self) -> str:
        """
        Retrieves the placeholder text for the username field.

        :return: Placeholder text for the username input field.
        """
        return self._driver.find_element(*self.l_user_name).get_attribute('placeholder')

    def get_password_hint(self) -> str:
        """
        Retrieves the placeholder text for the password field.

        :return: Placeholder text for the password input field.
        """
        return self._driver.find_element(*self.l_pw).get_attribute('placeholder')

    def login(self, user: str, pw: str) -> ProductsPage:
        """
        Performs a login using the provided username and password.

        Clears any existing inputs in the username and password fields, enters the new credentials,
        and clicks the login button to proceed to the Products Page.

        :param user: The username to enter in the login form.
        :param pw: The password to enter in the login form.
        :return: ProductsPage object representing the products page after login.
        """
        self.clear_username()
        self._driver.find_element(*HomePage.l_user_name).send_keys(user)
        self.clear_password()
        self._driver.find_element(*HomePage.l_pw).send_keys(pw)
        self._driver.find_element(*HomePage.l_login_btn).click()
        return ProductsPage(self._driver)

    def clear_username(self):
        """
        Clears the username input field.

        :return: None
        """
        return self._driver.find_element(*HomePage.l_user_name).clear()

    def clear_password(self):
        """
        Clears the password input field.

        :return: None
        """
        return self._driver.find_element(*HomePage.l_pw).clear()

    def get_login_error_message(self) -> str:
        """
        Fetches the error message displayed after a failed login attempt.

        :return: The login error message as a string.
        """
        return self._driver.find_element(*HomePage.l_err_msg).text

    def clear_login_error_message(self):
        """
        Clears the login error message by clicking the error button (usually an 'X' button).

        :return: None
        """
        return self._driver.find_element(*HomePage.l_err_msg_btn).click()

    # TODO: see it this method in necessary , otherwise remove it .
    def clear_all_login_data(self):
        """
        Clears all login data (username, password, and error message if any).

        :return: None
        """
        self._driver.find_element(*HomePage.l_user_name).clear()
        self._driver.find_element(*HomePage.l_pw).clear()
        self._driver.find_element(*HomePage.l_err_msg_btn).click()
