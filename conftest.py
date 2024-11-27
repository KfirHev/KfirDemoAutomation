import os
import json
import time
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from allure_commons._allure import label
import logging

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)

# Constants
RUN_LABEL_FILE = "Reports/run_label.txt"


def get_next_run_label():
    """
    Generate the next serial number for the test run.

    If the label file exists, reads the current label, increments it, and writes the updated label back to the file.
    If the file doesn't exist, starts with a default label of 0.

    Returns:
        int: The next run label.
    """
    if os.path.exists(RUN_LABEL_FILE):
        with open(RUN_LABEL_FILE, "r") as file:
            current_label = int(file.read().strip())
    else:
        current_label = 0

    next_label = current_label + 1

    with open(RUN_LABEL_FILE, "w") as file:
        file.write(str(next_label))

    return next_label


def create_executor_file(allure_results_dir, run_label):
    """
    Create an executor.json file in the specified allure-results directory.

    Args:
        allure_results_dir (str): The directory path where the executor.json file will be created.
        run_label (int): The label representing the current test run.

    Returns:
        None
    """
    executor_data = {
        "reportName": f"Run #{run_label}",
        "buildOrder": run_label,
        "reportUrl": "",
        "name": "Local",
        "type": "Local",
        "buildName": f"Build {run_label}"
    }
    executor_file_path = os.path.join(allure_results_dir, "executor.json")
    os.makedirs(allure_results_dir, exist_ok=True)
    with open(executor_file_path, "w") as file:
        json.dump(executor_data, file, indent=4)
    logger.info(f"Executor file created: {executor_file_path}")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """
    Generate and set the run label at the start of the test session.

    Also creates an executor.json file in the allure results directory.

    Args:
        session (Session): The pytest session object.

    Returns:
        None
    """
    global global_run_label
    global_run_label = get_next_run_label()
    logger.info(f"Run label for this session: {global_run_label}")
    label(session, "build", str(global_run_label))

    allure_results_dir = os.environ.get("ALLURE_RESULTS_PATH", "Reports/allure-results/default")
    logger.info(f"Using allure results directory: {allure_results_dir}")

    create_executor_file(allure_results_dir, global_run_label)


def pytest_addoption(parser):
    """
    Add custom command-line options for pytest.

    Args:
        parser (Parser): The pytest parser object for adding custom options.

    Returns:
        None
    """
    parser.addoption(
        "--browser_type", action="store", default="chrome", help="Specify the browser: chrome, firefox, or edge"
    )
    parser.addoption(
        "--run_env", action="store", default="local", help="Specify the environment: local or docker"
    )


def setup_browser_options(browser, run_env):
    """
    Set up browser-specific options based on the browser type and environment.

    Args:
        browser (str): The browser type ('chrome', 'firefox', 'edge').
        run_env (str): The environment ('local' or 'docker').

    Returns:
        Options: The configured browser options.
    """
    options = None
    if browser == "chrome":
        options = ChromeOptions()
        if run_env == "docker":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        else:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-autofill")
            options.add_argument("--disable-autocomplete")
    elif browser == "firefox":
        options = FirefoxOptions()
        options.headless = run_env == "docker"
    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("start-maximized")
        if run_env == "docker":
            options.add_argument("headless")
            options.add_argument("--disable-gpu")
    return options


@pytest.fixture(scope="class")
def setup_browser(request):
    """
    Set up the WebDriver instance for the specified browser and environment.

    Args:
        request (FixtureRequest): The pytest request object.

    Yields:
        WebDriver: The initialized WebDriver instance.
    """
    browser_name = request.config.getoption("browser_type")
    run_env = request.config.getoption("run_env")
    driver = None

    if run_env == "local":
        logger.info("Running LOCAL")
        if browser_name == "chrome":
            service = ChromeService(r"browserdriver/chromedriver130.exe")
            driver = webdriver.Chrome(service=service, options=setup_browser_options(browser_name, run_env))
        elif browser_name == "firefox":
            service = FirefoxService("C:/browserdriver/geckodriver.exe")
            driver = webdriver.Firefox(service=service, options=setup_browser_options(browser_name, run_env))
        elif browser_name == "edge":
            service = EdgeService("C:/browserdriver/msedgedriver.exe")
            driver = webdriver.Edge(service=service, options=setup_browser_options(browser_name, run_env))
    elif run_env == "docker":
        logger.info("Running in DOCKER")
        if browser_name in ["chrome", "firefox", "edge"]:
            driver = webdriver.Remote(
                command_executor="http://localhost:4444",
                options=setup_browser_options(browser_name, run_env),
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
    """
    Configure pytest to set up the HTML report file with a timestamp.

    Args:
        config (Config): The pytest configuration object.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = "Reports"
    os.makedirs(report_dir, exist_ok=True)
    report_filename = os.path.join(report_dir, f"Report_{timestamp}.html")
    config.option.htmlpath = report_filename
