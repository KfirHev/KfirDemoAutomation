import inspect
import os
from logging.handlers import RotatingFileHandler

import pytest
import logging
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures('setup_browser')
class BaseClass:

    @staticmethod
    def get_logger():

        logger_name = inspect.stack()[1][3]   # This command setting the logger name to the name of the calling method
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
        formater = logging.Formatter('%(asctime)s :%(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formater)

        # Add the handler to the logger
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def verify_link_clickable(self, locator):

        WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable(locator))

    def verify_link_presence(self, locator):

        WebDriverWait(self._driver, 10).until(EC.presence_of_element_located(locator))

    def select_from_dropdown(self, locator, value):

        dropdown = Select(self._driver.find_element(*locator))

        try:
            dropdown.select_by_visible_text(value)
        except NoSuchElementException as e:
            raise NoSuchElementException(f'Unknown value: {value}') from e



