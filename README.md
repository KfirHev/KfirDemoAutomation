# KfirDemoAutomation

![image](https://github.com/user-attachments/assets/b9a498af-d6a8-438d-8784-ee8cfcc03bdc)


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
---

**Note:** The `Logs/`, `Reports/`, and `Screenshots/` directories are git ignored due to the frequent generation of files that are not necessary for version control.


## Getting Started
**Example ETE test**

![TestFullPurchas](https://github.com/user-attachments/assets/37226fe2-e876-40e3-be14-ed91e3a1c0cf)


### Prerequisites
- **Python 3.x**  
- **Selenium WebDriver**  
- **Docker** (optional, for containerized tests)  

### Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/KfirHev/KfirDemoAutomation.git
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

**Example run via PyCharm**

https://github.com/user-attachments/assets/d38be0c4-8d73-4655-af75-31a1b375bab2

### Running Tests

1. **To run tests from the command line using Python's virtual environment**:
   - First, activate the virtual environment by running `. \YourProjectName\.venv\Scripts\activate`.
   - Then, execute the tests by typing `pytest`. (For customization options, refer to the options section below.)

2. **To run tests in a Docker container**:
   - Build the Docker image and run the container.

**Customizable Options**:
- Use `--browser_type` to specify the browser (default is chrome; other options include firefox and edge).
- Use `--run_env` to choose the environment (default is local; you can also select docker).

### View Reports

#### HTML Reports

1. Browse to the project Reports folder and choose the report ,you can drag and drop it to any browser to view it.

2. The HTML report name represent the date & time of the run.

3. The report include all the run data for each test case and their status

4. Upon failure the report will include the screenshot when it failed and the specific error logs

#### Jenkins Reports 

1. Access Jenkins: Open your Jenkins instance and navigate to the project for which the tests were executed.

2. View Report in Jenkins:
 - Locate the “Build History” section and select the specific build you want to analyze.
 - Inside the build details, you can find links to test reports, typically labeled as “Test Results” or under “HTML Publisher Plugin” if configured.
3. Detailed Test Analysis: The Jenkins report displays test statuses, including any test failures, along with logs. You’ll also see an option to view error screenshots and logs for failed tests if configured to save these artifacts.
4. Trend Analysis: Jenkins provides a view of historical test data, helping track trends in test pass/fail rates over time, enabling insights into project quality and stability.


## Planned Enhancements

Future updates will aim to extend the functionality and robustness of this framework, with potential additions including:

- Demonstration of API testing and backend database integration
- Enhanced reporting capabilities, such as Allure integration for richer test insights
- Detailed README updates, including Docker command instructions ,setting up Jenkins job/pipeline and example screenshots for a clearer demo experience 

## Contributing

This project is designed for demonstration purposes and is currently set as read-only for showcasing the framework’s capabilities. Contributions are not open at this time, but feel free to explore and use the code as a reference for similar projects.

