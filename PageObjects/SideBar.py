from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass


class SideBar(BaseClass):
    """
    Page object model for the Sidebar.

    This class provides methods to interact with the sidebar of the application,
    such as logging out and resetting the application state.
    """

    # Locators for elements in the Sidebar
    l_log_out = (By.ID, "logout_sidebar_link")
    l_reset_app_state = (By.ID, "reset_sidebar_link")

    def __init__(self, driver):
        """
        Initializes the SideBar object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the sidebar elements.
        """
        super().__init__()
        self._driver = driver

    def log_out(self):
        """
        Logs out of the application by clicking the log out link in the sidebar.

        This method locates the 'log out' button within the sidebar and clicks it.
        """
        # Locate and click the log-out button in the sidebar
        self._driver.find_element(*SideBar.l_log_out).click()

    def reset_app_and_logout(self):
        """
        Resets the application state and logs out.

        This method first resets the application to a clean state (removing all session data),
        then proceeds to log out of the application.
        """
        # Click the reset application state button in the sidebar to clear data
        self._driver.find_element(*SideBar.l_reset_app_state).click()

        # After resetting the app, log out of the application
        self.log_out()
