import os
from datetime import datetime
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


driver = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# This method is for creation of --browser_type option when running for cmd (can be set under pycharm config also)
def pytest_addoption(parser):
    parser.addoption(
        "--browser_type", action="store", default="chrome", help="my option: chrome or firefox or edge"
    )


@pytest.fixture(scope='class')
def setup_browser(request):
    browser_name = request.config.getoption('browser_type')

    if browser_name.lower() == 'chrome':
        global driver
        print('Chrome')
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--ignore-certificate-errors')
        # Specify the path to the ChromeDriver executable
        service = ChromeService("C:\\browserdriver\\chromedriver.exe")
        # Initialize the WebDriver with the Service object and use headless
        driver = webdriver.Chrome(service=service, options=chrome_options)
    elif browser_name.lower() == 'firefox':
        print('FireFox')
        firefox_options = FirefoxOptions()
        # Uncomment the line below if you want to run Firefox in headless mod
        # firefox_options.headless = True
        # Example of setting a preference
        # firefox_options.set_preference('dom.disable_open_during_load', True)
        service = FirefoxService("C:\\browserdriver\\geckodriver.exe")
        driver = webdriver.Firefox(service=service, options=firefox_options)
    elif browser_name.lower() == 'edge':
        print('Edge')
        edge_options = EdgeOptions()
        # edge_options.add_argument('--headless')
        edge_options.add_argument('--start-maximized')
        edge_options.add_argument('--ignore-certificate-errors')
        service = EdgeService("C:\\browserdriver\\msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=edge_options)
    else:
        raise ValueError("You should choose browser between chrome ,firefox or Edge")

    # Implicit wait for MAX TIMEOUT X sec
    driver.implicitly_wait(4)
    # Open the desired website
    # TODO setup landing page as a parameter - IN JENKINS ?
    driver.get("https://rahulshettyacademy.com/angularpractice/")
    # driver.get("https://rahulshettyacademy.com/upload-download-test/")   # for testing with excell
    # Attach the driver to the class
    request.cls.driver = driver

    yield
    #time.sleep(5)
    driver.close()


def pytest_configure(config):
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = 'Reports'
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"{report_dir}/report_{timestamp}.html"

    # Store the report filename in the pytest configuration
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
        # Ensure the directory exists
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Ensure not to overwrite existing file , adding index
        if os.path.exists(file_path):
            file_name, file_extension = os.path.splitext(file_path)
            index = 1
            while os.path.exists(file_path):
                file_path = f"{file_name}_{index}{file_extension}"
                index += 1
        # Capture the screenshot
        driver.get_screenshot_as_file(file_path)
        logger.info(f"Screenshot saved to {file_path}")

    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed a screenshot in the HTML report whenever a test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    logger.info(f"Report status: {report.when} - {report.outcome}")

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            # set path for failure screenshot to be located in Screenshots folder
            file_path = file_name.replace('Tests', 'Screenshots')

            logger.info(f"Capturing screenshot for {report.nodeid} to {file_path}")

            # Capture the screenshot to the Screenshot directory (path is relative to the framework pj
            screen_shots_path = 'Reports/' + file_path
            _capture_screenshot(screen_shots_path)

            # Embed screenshot in HTML report  (path is relative to the HTML report)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_path
                extra.append(pytest_html.extras.html(html))
            report.extra = extra
