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

driver = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# This method is for creation of --browser_type option when running for cmd (can be set under pycharm config also)
def pytest_addoption(parser):
    parser.addoption(
        "--browser_type", action="store", default="chrome", help="my option: chrome,firefox or edge"
    )
    parser.addoption(
        "--run_env", action="store", default="local", help="my option: local or docker"
    )


@pytest.fixture(scope='class')
def setup_browser(request):
    # global driver
    browser_name = request.config.getoption('browser_type')
    run_env = request.config.getoption('run_env')

    # Common browser setup
    def setup_chrome():
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--ignore-certificate-errors')
        # Updated Chrome path to run in the container
        # chrome_path = r"C:\Program Files\Chrome\chrome-win64\chrome.exe"
        # chrome_options.binary_location = chrome_path
        # return chrome_options

    def setup_firefox():
        firefox_options = FirefoxOptions()
        # Uncomment the line below if you want to run Firefox in headless mode
        firefox_options.headless = True
        return firefox_options

    def setup_edge():
        edge_options = EdgeOptions()
        edge_options.add_argument('--start-maximized')
        edge_options.add_argument('--ignore-certificate-errors')
        return edge_options

    # Local environment setup
    if run_env == 'local':
        if browser_name.lower() == 'chrome':
            print('Chrome - Local')
            chrome_options = ChromeOptions()
            #chrome_options.add_argument('--no-sandbox')
            #chrome_options.add_argument('--headless=new')
            #chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--start-maximized')
            #chrome_options.add_argument('--ignore-certificate-errors')
            #chrome_options = setup_chrome()
            #chrome_path = r"C:\Program Files\Chrome\chrome-win64\chrome.exe"
            #chrome_options.binary_location = chrome_path
            # set the user-agent back to chrome.
            user_agent = 'Chrome/129.0.6668.59'
            chrome_options.add_argument(f'user-agent={user_agent}')
            # TODO: Modify for Windows or Linux based on your platform
            #service = ChromeService(r"C:\Program Files\Chrome\ChromeDriver\chromedriver-win64\chromedriver.exe")
            # TODO FOR LOCAL WINDOWS:
            service = ChromeService(r"browserdriver\\chromedriver128.exe")
            driver = webdriver.Chrome(service=service, options=chrome_options)


        elif browser_name.lower() == 'firefox':
            print('FireFox - Local')
            firefox_options = setup_firefox()
            # TODO: Modify for Windows or Linux based on your platform
            service = FirefoxService(r"browserdriver\\geckodriver.exe")  # Windows path example
            driver = webdriver.Firefox(service=service, options=firefox_options)

        elif browser_name.lower() == 'edge':
            print('Edge - Local')
            edge_options = setup_edge()
            # TODO: Modify for Windows or Linux based on your platform
            service = EdgeService(r"browserdriver\\msedgedriver.exe")  # Windows path example
            driver = webdriver.Edge(service=service, options=edge_options)

        else:
            raise ValueError("You should choose a browser between chrome, firefox, or edge")

    # Docker/Grid environment setup
    elif run_env == 'docker':
        if browser_name.lower() == 'chrome':
            print('Chrome - Docker')
            chrome_options = setup_chrome()
            driver = webdriver.Remote(
                command_executor="http://selenium-hub:4444/wd/hub",
                options=chrome_options
            )

        elif browser_name.lower() == 'firefox':
            print('FireFox - Docker')
            firefox_options = setup_firefox()
            driver = webdriver.Remote(
                command_executor="http://selenium-hub:4444/wd/hub",
                options=firefox_options
            )

        else:
            raise ValueError("Only Chrome and Firefox are supported in Docker")

    else:
        raise ValueError("You should choose the environment between local and docker")

    # Implicit wait for MAX TIMEOUT X sec
    driver.implicitly_wait(4)

    # Open the desired website (can be parameterized later)
    driver.get("https://www.saucedemo.com/")

    # Attach the driver to the class
    request.cls.driver = driver

    yield
    time.sleep(4)  # for demo purposes
    driver.quit()


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
