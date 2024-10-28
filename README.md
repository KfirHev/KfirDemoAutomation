# KfirDemoAutomation

**An automation framework for testing [SauceDemo](https://www.saucedemo.com/) with Selenium and pytest in Python.**  
Designed for high flexibility and modularity, the framework facilitates efficient browser-based testing and provides HTML reports with screenshots and logging for thorough test insights. **This framework's infrastructure can support any web-based application** with some modifications.


---

## Features

- **HTML Reports with Screenshots**: Automatically generated HTML reports with embedded failure screenshots.  
- **Logging Mechanism**: Comprehensive logs of each test run, rotated for efficient storage management.  
- **Data-Driven Testing**: Supports Python dictionaries for test data input.  
- **Docker Compatibility**: Run tests in isolated Docker environments.  
- **Extensible BaseClass**: Streamlines test development, minimizes code redundancy.  

---

## Project Structure

```plaintext
KfirDemoAutomation/  
├── .venv/  
│       Python virtual environment (git ignored)  
│  
├── browserdriver/  
│       WebDriver executables for supported browsers  
│  
├── Logs/  
│       Folder for log files, generated at runtime (git ignored)  
│  
├── PageObjects/  
│       Page classes containing element locators and actions  
│  
├── Reports/  
│       HTML test reports with embedded failure screenshots (git ignored)  
│  
├── Screenshots/  
│       Failure screenshots for reports, dynamically generated (git ignored)  
│  
├── Templates/  
│       Test templates to aid test creation  
│  
├── TestData/  
│       Dictionary-style test data for data-driven tests  
│  
├── Tests/  
│       Test scripts organized by feature (e.g., login, products)  
│   └── conftest.py  
│       Setup and teardown, browser configuration  
│  
├── Utils/  
│       BaseClass with common utilities and locators to avoid redundancy  
│  
├── Dockerfile  
│       Configuration for containerized testing  
│  
└── requirements.txt  
        Python dependencies for the project

## Getting Started
## Prerequisites
Python 3.x
Selenium WebDriver
Docker (optional, for containerized tests) 
