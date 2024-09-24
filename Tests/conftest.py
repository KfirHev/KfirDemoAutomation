import os
import time
from datetime import datetime
import pytest
import logging
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Global driver instance
driver = None

# Set up logging for the test framework
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """
    Adds command-line options for browser type and environment to pytest.

    Args:
        parser: The parser object to add command-line options.
    """
    parser.addoption(
        "--browser_type", action="store", default="chrome", help="Specify the browser: chrome, firefox, or edge"
    )
    parser.addoption(
        "--run_env", action="store", default="local", help="Specify the environment: local or docker"
    )


@pytest.fixture(scope='class')
def setup_browser(request):
    """
    Pytest fixture that sets up the browser driver before each test class is run.

    Args:
        request: Pytest fixture request object to access test-specific data.

    Yields:
        Yields the initialized browser driver and quits the driver after the tests finish.
    """
    global driver
    browser_name = request.config.getoption('browser_type')
    run_env = request.config.getoption('run_env')

    # Set up browser based on the environment and browser type
    if run_env == 'local':
        if browser_name.lower() == 'chrome':
            print('Chrome - Local')
            chrome_options = ChromeOptions()
            # Uncomment below line to run tests in headless mode
            # chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--ignore-certificate-errors')
            service = ChromeService(r"browserdriver\\chromedriver128.exe")
            driver = webdriver.Chrome(service=service, options=chrome_options)

        # Add cases for firefox and edge here if needed
        else:
            raise ValueError("You should choose a browser between chrome, firefox, or edge")

    # Set an implicit wait for elements
    driver.implicitly_wait(4)

    # Open the specified website (can be parameterized later)
    driver.get("https://www.saucedemo.com/")

    # Attach the driver to the class for use in test methods
    request.cls.driver = driver

    # Yield driver to the test class, and quit after all tests finish
    yield
    time.sleep(4)  # Pause for demo purposes
    driver.quit()


def pytest_configure(config):
    """
    Configures the test report settings, such as setting up the directory and file name for HTML reports.

    Args:
        config: Pytest config object to modify runtime settings.
    """
    # Generate a timestamp for the report file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = 'Reports'
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"{report_dir}/report_{timestamp}.html"

    # Store the HTML report path in the pytest configuration
    config.option.htmlpath = report_filename


def _capture_screenshot(file_path):
    """
    Captures a screenshot of the current browser window and saves it to the specified file path.

    If a file already exists at the given path, this function appends an index to the file name
    (e.g., 'file_1.png', 'file_2.png') to avoid overwriting the existing file.

    Args:
        file_path (str): The full path where the screenshot should be saved, including the file name and extension.

    Raises:
        Exception: If there is an error during the screenshot capture process, the exception is logged.

    Example:
        _capture_screenshot('screenshots/test.png')
        This will save the screenshot as 'test.png', or 'test_1.png' if 'test.png' already exists.
    """
    try:
        # Ensure the directory for screenshots exists
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Avoid overwriting existing screenshot files by appending an index to the filename
        if os.path.exists(file_path):
            file_name, file_extension = os.path.splitext(file_path)
            index = 1
            while os.path.exists(file_path):
                file_path = f"{file_name}_{index}{file_extension}"
                index += 1

        # Capture the screenshot using the global WebDriver instance
        driver.get_screenshot_as_file(file_path)
        logger.info(f"Screenshot saved to {file_path}")

    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook that captures and embeds a screenshot into the HTML report if a test fails.

    Args:
        item: The pytest test item being reported.
    """
    # Access the HTML plugin for report generation
    pytest_html = item.config.pluginmanager.getplugin('html')

    # Run the test and get the result
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    logger.info(f"Report status: {report.when} - {report.outcome}")

    # If the test failed or was skipped, capture a screenshot
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Set the screenshot file path
            file_name = report.nodeid.replace("::", "_") + ".png"
            file_path = file_name.replace('Tests', 'Screenshots')

            logger.info(f"Capturing screenshot for {report.nodeid} to {file_path}")

            # Capture the screenshot and save it to the Reports folder
            screen_shots_path = 'Reports/' + file_path
            _capture_screenshot(screen_shots_path)

            # Embed the screenshot in the HTML report (path relative to the HTML report)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_path
                extra.append(pytest_html.extras.html(html))
            report.extra = extra
