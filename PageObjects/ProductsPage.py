import time

from selenium.webdriver.common.by import By

from PageObjects.CheckOutInfoPage import CheckOutInfoPage
from Utils.BaseClass import BaseClass
from PageObjects.SingleProductPage import SingleProductPage


class ProductsPage(BaseClass):
    """Page object model for the Products Page, handling product interactions and cart management."""

    # Locators for elements on the Products Page
    l_all_page_products_names = (By.CSS_SELECTOR, ".inventory_item_name")
    l_all_page_products_prices = (By.CSS_SELECTOR, ".inventory_item_price")
    l_add_to_cart_buttons = (By.XPATH, "//button[text() = 'Add to cart']")
    l_remove_from_cart_buttons = (By.XPATH, "//button[text() = 'Remove']")
    l_sort_dropdown = (By.CSS_SELECTOR, ".product_sort_container")
    l_checkout_button = (By.ID, 'checkout')

    def __init__(self, driver):
        """
        Initializes the ProductsPage object with the WebDriver instance and a SideBar instance.

        :param driver: WebDriver instance for interacting with the page elements.
        """
        super().__init__()
        self._driver = driver

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

    def remove_all_products_from_the_cart(self):
        """
        Removes all visible products from the cart by clicking on each "Remove" button.
        """
        remove_from_cart_buttons = self._driver.find_elements(*ProductsPage.l_remove_from_cart_buttons)
        for button in remove_from_cart_buttons:
            button.click()

    def add_product_to_cart(self, product_name):
        """Add product to the cart by its name."""
        self._add_or_remove_products(product_name, action="add")

    def remove_product_from_cart(self, product_name):
        """Remove product from the cart by its name."""
        self._add_or_remove_products(product_name, action="remove")

    def _add_or_remove_products(self, product_name, action):
        """
        Adds or removes product(s) from the cart based on the action.

        Identifies the button dynamically by the product name and performs the specified action
        (either 'add' or 'remove').

        :param product_name: List of product names to be added or removed.
        :param action: Action to perform - 'add' or 'remove'.
        """
        for product in product_name:
            product_formatted = product.lower().replace(' ', '-')
            if action == 'add':
                btn_id = f"add-to-cart-{product_formatted}"
            else:  # remove
                btn_id = f"remove-{product_formatted}"
            self._driver.find_element(By.ID, btn_id).click()

    def check_if_product_added(self, product_name):
        """
        Checks if a specific product is added to the cart by looking for the remove button.

        :param product_name: The name of the product to check for.
        :return: The WebElement representing the remove button if found, otherwise raises an exception.
        """
        # Construct the ID for the remove button by formatting the product name
        l_remove_btn_by_name = f"remove-{product_name.lower().replace(' ', '-')}"
        return self._driver.find_element(By.ID, l_remove_btn_by_name)

    def click_product_by_name(self, product_name):
        """
        Clicks on a product link by its name to navigate to the product's detail page.

        :param product_name: The name of the product to click on.
        :return: An instance of the SingleProductPage class after the click action.
        """
        # Click the product link directly using the link text
        self._driver.find_element(By.LINK_TEXT, product_name).click()
        return SingleProductPage(self._driver)

    def sort_products_by(self, sorting_option):
        """
        Selects a sorting option from the dropdown to sort the products displayed on the page.

        :param sorting_option: The sorting option to be selected (e.g., 'Name (A to Z)', 'Price (low to high)').
        """
        # Click on the sort dropdown and select the desired option
        self._driver.find_element(*ProductsPage.l_sort_dropdown).click()
        self._driver.find_element(By.XPATH, f"//option[text()='{sorting_option}']").click()

    def verify_sorting_is_correct(self, sorting_option):
        """
        Verifies that the products are sorted correctly based on the selected sorting option.

        :param sorting_option: The sorting option used for verification.
        :return: True if the sorting is correct, False otherwise.
        """
        # Retrieve the product names and prices from the page
        products_names = self._driver.find_elements(*ProductsPage.l_all_page_products_names)
        products_prices = self._driver.find_elements(*ProductsPage.l_all_page_products_prices)

        # Check sorting correctness based on the selected option
        if sorting_option == 'Name (Z to A)':
            product_list = [pr.text for pr in products_names]
            return product_list == sorted(product_list, reverse=True)

        elif sorting_option == 'Name (A to Z)':
            product_list = [pr.text for pr in products_names]
            return product_list == sorted(product_list)

        elif sorting_option == 'Price (low to high)':
            product_list = [float(pr.text.strip('$')) for pr in products_prices]
            return product_list == sorted(product_list)

        elif sorting_option == 'Price (high to low)':
            product_list = [float(pr.text.strip('$')) for pr in products_prices]
            return product_list == sorted(product_list, reverse=True)

    def checkout(self):
        self._driver.find_element(*ProductsPage.l_checkout_button).click()
        return CheckOutInfoPage(self._driver)
