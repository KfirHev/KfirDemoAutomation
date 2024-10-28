import time
from selenium.webdriver.common.by import By
from Utils.BaseClass import BaseClass
from PageObjects.SingleProductPage import SingleProductPage


class ProductsPage(BaseClass):
    """
    Page object model for the Products Page, handling product interactions and cart management.

    This class includes methods to interact with products, add or remove items from the cart,
    sort products, and navigate to the checkout page. Each method is designed to be reusable
    for various tests involving the Products Page.
    """

    # Locators for elements on the Products Page
    l_all_products = (By.CSS_SELECTOR, ".inventory_item")
    l_all_page_products_names = (By.CSS_SELECTOR, ".inventory_item_name")
    l_all_product_description = (By.CSS_SELECTOR, ".inventory_item_desc")
    l_all_page_products_prices = (By.CSS_SELECTOR, ".inventory_item_price")
    l_add_to_cart_buttons = (By.XPATH, "//button[text() = 'Add to cart']")
    l_remove_from_cart_buttons = (By.XPATH, "//button[text() = 'Remove']")
    l_sort_dropdown = (By.CSS_SELECTOR, ".product_sort_container")

    def __init__(self, driver):
        """
        Initializes the ProductsPage object

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

    def get_product_info(self, product_name):
        """
        Retrieves the details, price, and image source for a given product.

        :param product_name: The name of the product to retrieve information for.
        :return: A tuple containing product details (description), price, and image URL.
        """
        products = self._driver.find_elements(*ProductsPage.l_all_products)
        for product in products:
            if product_name in product.text:
                product_image = self._driver.find_element(By.CSS_SELECTOR, f"img[alt='{product_name}']")
                image_src = product_image.get_attribute('src')
                info = product.text.split('\n')
                product_details = info[1]
                product_price = info[2]
                return product_details, product_price, image_src

    def get_product_details(self, product_name):
        """
        Fetches the product details for a given product.

        :param product_name: The name of the product to get details for.
        :return: The product description as a string.
        """
        return self.get_product_info(product_name)[0]

    def get_product_price(self, product_name):
        """
        Fetches the price for a given product.

        :param product_name: The name of the product to get the price for.
        :return: The product price as a string.
        """
        return self.get_product_info(product_name)[1]

    def get_product_image(self, product_name):
        """
        Fetches the image URL for a given product.

        :param product_name: The name of the product to get the image URL for.
        :return: The URL of the product image as a string.
        """
        return self.get_product_info(product_name)[2]

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
        """
        Adds a specific product to the cart based on the product name.

        :param product_name: The name of the product to add to the cart.
        """
        self._add_or_remove_products(product_name, action="add")

    def remove_product_from_cart(self, product_name):
        """
        Removes a specific product from the cart based on the product name.

        :param product_name: The name of the product to remove from the cart.
        """
        self._add_or_remove_products(product_name, action="remove")

    def _add_or_remove_products(self, product_name, action):
        """
        Adds or removes product(s) from the cart based on the specified action.

        :param product_name: The name or list of names of products to add or remove.
        :param action: The action to perform, either "add" or "remove".
        """
        if type(product_name) is str:  # handle cases where a single name is sent
            product_name = [product_name]
        for product in product_name:
            product_formatted = product.lower().replace(' ', '-')
            if action == 'add':
                btn_id = f"add-to-cart-{product_formatted}"
            else:  # remove
                btn_id = f"remove-{product_formatted}"
            self._driver.find_element(By.ID, btn_id).click()

    def check_if_product_added(self, product_name):
        """
        Checks if a specific product has been added to the cart by looking for the remove button.

        :param product_name: The name of the product to check for.
        :return: The WebElement representing the remove button if found.
        :raises NoSuchElementException: If the remove button for the product is not found.
        """
        l_remove_btn_by_name = f"remove-{product_name.lower().replace(' ', '-')}"
        return self._driver.find_element(By.ID, l_remove_btn_by_name)

    def click_product_by_name(self, product_name):
        """
        Clicks on a product by its name to navigate to its detail page.

        :param product_name: The name of the product to click on.
        :return: An instance of the SingleProductPage class.
        """
        self._driver.find_element(By.LINK_TEXT, product_name).click()
        return SingleProductPage(self._driver)

    def sort_products_by(self, sorting_option):
        """
        Sorts the products displayed on the page by a given sorting option.

        :param sorting_option: The sorting option to select (e.g., 'Name (A to Z)', 'Price (low to high)').
        """
        self._driver.find_element(*ProductsPage.l_sort_dropdown).click()
        self._driver.find_element(By.XPATH, f"//option[text()='{sorting_option}']").click()

    def verify_sorting_is_correct(self, sorting_option):
        """
        Verifies that the products are sorted correctly based on the selected sorting option.

        :param sorting_option: The sorting option used for verification.
        :return: True if the products are sorted correctly, False otherwise.
        """
        products_names = self._driver.find_elements(*ProductsPage.l_all_page_products_names)
        products_prices = self._driver.find_elements(*ProductsPage.l_all_page_products_prices)

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
