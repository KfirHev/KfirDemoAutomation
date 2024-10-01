from selenium.webdriver.common.by import By
from PageObjects.SideBar import SideBar
from Utils.BaseClass import BaseClass


class CartPage(BaseClass):
    """Page object model for the Cart Page."""

    # Locators for elements on the Cart Page
    l_side_menu_button = (By.ID, "react-burger-menu-btn")  # TODO move it to baseclass
    l_all_page_products_names = (By.CSS_SELECTOR, ".inventory_item_name")
    l_continue_shopping_button = (By.ID, "continue-shopping")

    def __init__(self, driver):
        """
        Initializes the CartPage object with the WebDriver instance.

        :param driver: WebDriver instance for interacting with the page.
        """
        super().__init__()
        self._driver = driver
        # Initialize Sidebar for sidebar-related actions
        self._sidebar = SideBar(self._driver)

    def get_page_products_name(self):
        """
        Retrieves the names of all products displayed on the cart page.

        :return: A list of product names on the cart page.
        """
        # Using BaseClass method
        return self.get_products_name(CartPage.l_all_page_products_names)

    def continue_shopping(self):
        self._driver.find_element(*CartPage.l_continue_shopping_button).click()
        from PageObjects.ProductsPage import ProductsPage
        return ProductsPage(self._driver)

    def log_out(self):
        """
        Logs out of the application using the sidebar's log out method.

        This method first verifies the side menu button is displayed, then
        clicks the button to open the menu and logs out via the Sidebar object.

        :return: HomePage object representing the user being redirected to the home page.
        """
        # Verify the side menu button is visible before proceeding
        self.verify_element_displayed(CartPage.l_side_menu_button)

        # Open the sidebar by clicking the side menu button
        self._driver.find_element(*CartPage.l_side_menu_button).click()

        # Perform the logout using the sidebar
        self._sidebar.log_out()

        # Redirect back to the home page after logging out
        from PageObjects.HomePage import HomePage
        return HomePage(self._driver)

    def reset_application_state(self): # Todo move to BaseClass
        """
        Resets the application state by opening the sidebar and clearing the session.

        This method clicks the side menu button, then calls the reset function from the
        Sidebar class to reset the application state and log out.
        """
        # Open the sidebar by clicking the side menu button
        self._driver.find_element(*CartPage.l_side_menu_button).click()

        # Use the sidebar object to reset the app and log out
        self._sidebar.reset_app_and_logout()
