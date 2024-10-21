import time
import pytest
from PageObjects.HomePage import HomePage
from Utils.BaseClass import BaseClass


# @pytest.mark.skip
class TestLinkToX(BaseClass):
    """
    This test class verifies the functionality of the link to the external website X.

    Test Steps:
    1. Log in to the application using the homepage.
    2. Click the link that opens the external X page.
    3. Assert that the page title of the newly opened X page is correct.
    4. Verify that the text from the hover card is correct.
    5. Verify that the application returns to the original window (context switch).
    6. Reset the application state to ensure a clean slate for other tests.
    """

    @pytest.mark.skip
    def test_link_to_x(self):
        """
        Verifies that clicking the external link opens the correct X page,
        demonstrates switching to other windows, checks the text from the hover card,
        and resets the application state afterward.
        """

        log = self.get_logger()
        home_page = HomePage(self.driver)

        try:
            # Log into the application
            products_page = home_page.login()
            log.info("Login successful")

            # Click the link to X, retrieve the title and hover text, then close the new window
            title, hover_text = products_page.open_and_verify_link_to_x()
            assert title == 'Sauce Labs (@saucelabs) / X', "Failed to open https://x.com/saucelabs"
            log.info("Successfully opened the X page: https://x.com/saucelabs")

            # Verify the text from the first hover card in X
            assert 'organizations deliver a trusted digital experience' in hover_text, ("Failed to get data from "
                                                                                        "first X hover card")
            log.info("Successfully retrieved text from the first X hover card")

            # Verify back to the application window (Products page)
            title = products_page.get_page_title()
            assert title == 'Products', "Failed to return to the application window"
            log.info("Successfully returned to the application window")

            # Reset the application state to avoid side effects on other tests
            products_page.reset_application_state()
            log.info("Application state reset successful")

        except AssertionError as ae:
            # Log assertion errors
            log.error(f"Assertion failed: {ae}")
            raise

        except Exception as e:
            # Log any unexpected errors
            log.error(f"An error occurred during the test: {e}")
            raise

