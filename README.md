# KfirDemoAutomation

**An automation framework for testing [SauceDemo](https://www.saucedemo.com/) with Selenium and pytest.**  
Designed for high flexibility and modularity, the framework facilitates efficient browser-based testing and provides HTML reports with screenshots and logging for thorough test insights.  
This framework's infrastructure can support any web-based application with minimal modifications.  

## Project Structure

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

### Prerequisites
- **Python 3.x**  
- **Selenium WebDriver**  
- **Docker** (optional, for containerized tests)  

### Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/username/KfirDemoAutomation.git
    ```

2. Navigate into the project directory:
    ```bash
    cd KfirDemoAutomation
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. To run tests:
    ```bash
    pytest
    ```

2. To run tests in a Docker container:
    ```bash
    docker build -t kfirdemoautomation .
    docker run kfirdemoautomation
    ```

## Next Developments

Future improvements include adding:
- Additional browser support.
- Enhanced reporting features (Allure)
- CI/CD  E.g Jenkins jobs
- Improving this readme file , with container commands and demo screenshots 

## Contributing

This project is designed for demonstration purposes and is currently set as read-only for showcasing the framework’s capabilities. Contributions are not open at this time, but feel free to explore and use the code as a reference for similar projects.

---

**Note:** The `Logs/`, `Reports/`, and `Screenshots/` directories are git ignored due to the frequent generation of files that are not necessary for version control.
