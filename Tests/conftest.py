import os
import time
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

# Global driver instance
driver = None

# Set up logging for the test framework
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--browser_type", action="store", default="chrome", help="Specify the browser: chrome, firefox, or edge"
    )
    parser.addoption(
        "--run_env", action="store", default="local", help="Specify the environment: local or docker"
    )


# Browser Options for Local Run
def setup_chrome_options():
    options = ChromeOptions()
    options.add_argument('--headless=new')  # Uncomment for headless mode
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-autofill")
    options.add_argument("--disable-autocomplete")
    return options


def setup_firefox_options():
    options = FirefoxOptions()
    # options.headless = True  # Uncomment for headless mode
    return options


def setup_edge_options():
    options = EdgeOptions()
    # options.add_argument('headless')  # Uncomment for headless mode
    options.add_argument('start-maximized')
    return options


# Browser Options for Docker Run
def setup_docker_chrome_options():
    options = ChromeOptions()
    options.add_argument("--headless=new")  # Docker runs headless by default
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return options


def setup_docker_firefox_options():
    options = FirefoxOptions()
    options.headless = True
    return options


def setup_docker_edge_options():
    options = EdgeOptions()
    options.add_argument('headless')
    options.add_argument("--disable-gpu")
    return options


@pytest.fixture(scope='class')
def setup_browser(request):
    global driver
    browser_name = request.config.getoption('browser_type')
    run_env = request.config.getoption('run_env')

    # Local Run
    if run_env == 'local':
        if browser_name.lower() == 'chrome':
            service = ChromeService(r"browserdriver\\chromedriver129.exe")
            driver = webdriver.Chrome(service=service, options=setup_chrome_options())
        elif browser_name.lower() == 'firefox':
            service = FirefoxService("C:\\browserdriver\\geckodriver.exe")
            driver = webdriver.Firefox(service=service, options=setup_firefox_options())
        elif browser_name.lower() == 'edge':
            service = EdgeService("C:\\browserdriver\\msedgedriver.exe")
            driver = webdriver.Edge(service=service, options=setup_edge_options())
        else:
            raise ValueError("You should choose a browser between chrome, firefox, or edge")

    # Docker Run
    elif run_env == 'docker':
        if browser_name.lower() == 'chrome':
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                options=setup_docker_chrome_options()
            )
        elif browser_name.lower() == 'firefox':
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                options=setup_docker_firefox_options()
            )
        elif browser_name.lower() == 'edge':
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                options=setup_docker_edge_options()
            )
        else:
            raise ValueError("You should choose a browser between chrome, firefox, or edge")

    driver.implicitly_wait(4)
    driver.get("https://www.saucedemo.com/")
    request.cls.driver = driver

    yield
    time.sleep(4)
    driver.quit()


def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = 'Reports'
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"{report_dir}/Report_{timestamp}.html"
    config.option.htmlpath = report_filename


def _capture_screenshot(file_path):
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.exists(file_path):
            file_name, file_extension = os.path.splitext(file_path)
            index = 1
            while os.path.exists(file_path):
                file_path = f"{file_name}_{index}{file_extension}"
                index += 1

        driver.get_screenshot_as_file(file_path)
        logger.info(f"Screenshot saved to {file_path}")

    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            file_path = file_name.replace('Tests', 'Screenshots')

            screen_shots_path = 'Reports/' + file_path
            _capture_screenshot(screen_shots_path)

            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_path
                extra.append(pytest_html.extras.html(html))
            report.extra = extra
