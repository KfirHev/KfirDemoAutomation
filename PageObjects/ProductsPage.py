import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass
from PageObjects.CartPage import CartPage
from PageObjects.SideBar import SideBar
from PageObjects.SingleProductPage import SingleProductPage


class ProductsPage(BaseClass):
    """Page object model for the Products Page, handling product interactions and cart management."""

    # Locators for elements on the Products Page
    l_side_menu_button = (By.ID, "react-burger-menu-btn")  # TODO move it to baseclass
    l_title = (By.CSS_SELECTOR, ".title")
    l_all_page_products_names = (By.CSS_SELECTOR, ".inventory_item_name")
    l_add_to_cart_buttons = (By.XPATH, "//button[text() = 'Add to cart']")
    l_remove_from_cart_buttons = (By.XPATH, "//button[text() = 'Remove']")

    def __init__(self, driver):
        """
        Initializes the ProductsPage object with the WebDriver instance and a SideBar instance.

        :param driver: WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver
        # Initialize Sidebar for sidebar-related actions
        self._sidebar = SideBar(self._driver)

    def log_out(self):
        """
        Logs out of the application using the sidebar.

        Verifies if the side menu button is visible, then opens the sidebar and calls the log out function.

        :return: HomePage object to represent the redirection after logging out.
        """
        self.verify_element_displayed(ProductsPage.l_side_menu_button)
        self._driver.find_element(*ProductsPage.l_side_menu_button).click()
        self._sidebar.log_out()

        # Import HomePage to avoid circular imports
        from PageObjects.HomePage import HomePage
        return HomePage(self._driver)

    def reset_application_state(self):  # Todo move to BaseClass
        """
        Resets the application state through the sidebar.

        This method opens the sidebar and calls the reset function from the Sidebar class to clear the session.

        :param sidebar: Sidebar object used to reset the application state and log out.
        """
        self._driver.find_element(*ProductsPage.l_side_menu_button).click()
        self._sidebar.reset_app_and_logout()

    def get_page_title(self) -> str:
        """
        Retrieves the page header title.

        :return: The title of the products page header.
        """
        return self._driver.find_element(*ProductsPage.l_title).text

    def get_page_products_name(self):
        """
        Fetches the names of all products listed on the page.

        :return: A list of product names displayed on the products page.
        """
        return self.get_products_name(ProductsPage.l_all_page_products_names)

    def add_all_products_to_cart(self):
        """
        Adds all visible products to the cart by clicking on each "Add to cart" button.
        """
        add_to_cart_buttons = self._driver.find_elements(*ProductsPage.l_add_to_cart_buttons)
        for button in add_to_cart_buttons:
            button.click()

    def add_product_to_cart(self, product_name):
        """
        Adds a specific product to the cart based on the product's name.

        Extracts the product name from the button's ID and compares it with the given product name.
        If they match, the corresponding product is added to the cart.

        :param product_name: Name of the product to be added to the cart.
        """

        for product in product_name:
            product = product.replace('-', ' ')  # if the product name has - replace it with a space
            add_to_cart_buttons = self._driver.find_elements(*ProductsPage.l_add_to_cart_buttons)
            for button in add_to_cart_buttons:
                # Extract product name from the button's ID, ignoring the "add-to-cart" prefix
                name = button.get_attribute("id").split('-')[3:]
                name = ' '.join(name)
                if name == product.lower():
                    button.click()
                    break

    def check_if_product_added(self, product_name):
        # return if element is found
        l_remove_btn_by_name = f"remove-{product_name.lower().replace(' ', '-')}"
        return self._driver.find_element(By.ID, l_remove_btn_by_name)

    def click_product_by_name(self, product_name):

        # instead of looping through page products name use the direct link approach
        self._driver.find_element(By.LINK_TEXT, product_name).click()
        return SingleProductPage(self._driver)
