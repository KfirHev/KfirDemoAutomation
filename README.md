# KfirDemoAutomation

![image](https://github.com/user-attachments/assets/a5834843-359a-472a-a378-563882b884b8)

**An automation framework for testing [SauceDemo](https://www.saucedemo.com/) with Selenium and pytest.**  
It supports multi-browser testing, CI/CD pipelines, and containerization, offering scalable and flexible test execution. 
The framework generates multiple reports, including HTML and Allure, with detailed logs and screenshots.
It demonstrates functional, E2E, and performance testing and is easily adaptable to any web-based application.

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
**🚩Note:** The `Logs/`, `Reports/`, and `Screenshots/` directories are git ignored due to the frequent generation of files that are not necessary for version control.


## Getting Started
**Example ETE test**

![TestFullPurchas](https://github.com/user-attachments/assets/37226fe2-e876-40e3-be14-ed91e3a1c0cf)


### 🛠 Prerequisites
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

### Running Tests from Your Local Environment

**To run tests from the command line using Python's virtual environment**:
   - First, activate the virtual environment by running `. \YourProjectName\.venv\Scripts\activate`.
   - Then, execute the tests by typing `pytest`. (For customization options, refer to the options section below.)
   
### Runinng Tests in a Docker container or Docker Selenium Grid 

This project includes Docker configurations to simplify running the automation framework in various environments. It supports both local execution and remote execution using Selenium Grid.

Before proceeding, ensure you have **Docker Desktop** installed and running on your machine. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop/).

<details>
<summary>Click to expand for Docker Instructions</summary>

#### Docker Configurations

The project provides two Dockerfiles for different execution environments:

1. **Dockerfile_python**  
   - Used for running tests on a **Selenium Grid** setup.  
   - The browser (e.g., Chrome, Firefox, Edge) runs in a separate container.  
   - Run the project with the command-line option:  
     ```bash
     --run_env "docker"
     ```

2. **Dockerfile_all_in_one**  
   - Installs all necessary components, including project dependencies, ChromeDriver, and the Chrome browser.  
   - Ideal for running tests locally within the Docker container, without requiring Selenium Grid.

---

#### Setting Up Selenium Grid

To run tests remotely using Selenium Grid, you need to set up a Selenium Grid container with the desired browser(s). Follow these steps:

#### Pull the Selenium Grid Browser Images
Run the following commands to pull the required Docker images for Selenium Grid:

- **For Chrome:**
  ```bash
  docker pull selenium/standalone-chrome:latest
- **For Firefox:**
  ```bash
  docker pull selenium/standalone-firefox:latest
- **For Edge:**
  ```bash
  docker pull selenium/standalone-edge:latest
  
#### Run the Selenium Grid Containers

Start the container for your desired browser:

- **For Chrome ,FireFox, Edge:**
  ```bash
  docker run --rm -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest
  docker run --rm -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:latest
  docker run --rm -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-edge:latest

**You can open the Selenium Grid app and watch it run on your browser using [http://localhost:4444/](http://localhost:4444/)**

#### Building and Running the Project Containers

1. **Building the Image**  
   Navigate to the project directory and build the Docker image based on the desired configuration:

   - **For `Dockerfile_python`:**
     ```bash
     docker build -f Dockerfile_python -t your_env_name_image .
     ```

   - **For `Dockerfile_all_in_one`:**
     ```bash
     docker build -f Dockerfile_all_in_one -t your_env_name_image .
     ```

2. **Running the Container**  
   Run the Docker container interactively:

   ```bash
     docker run --network="host" -it your_env_name_image
   
    ```
 **For Selenium Grid Setup: Use the Dockerfile_python image and ensure the Selenium Grid container(s) for your desired browser(s) are running.**
 
 **For Local Execution: Use the Dockerfile_all_in_one image, which includes ChromeDriver and Chrome for standalone execution.**
</details> 

**Customizable Options**:
- Use `--browser_type` to specify the browser (default is chrome; other options include firefox and edge).
- Use `--run_env` to choose the environment (default is local; you can also select docker).

### Running Tests Using Jenkins (** instructions will follow in the near future)
To run tests using Jenkins, follow these steps to set up the environment and configure the necessary Jenkins job. This process will work no matter where your app is located, as long as the required dependencies are met.

#### Prerequisites

- **Jenkins installed and running** (either on a local instance or remote server).
- **Docker installed** on the machine running Jenkins (if you are using Docker for test execution).
- **GitHub repository** (or other source control) connected to Jenkins.
- **Docker images** for your project built and pushed to a registry or available locally.

<details>
<summary>Click to expand for Jenkins Instructions</summary>
(Instructions will follow in the near future)
</details> 


### View Reports


https://github.com/user-attachments/assets/c686d899-91cc-4702-9b9a-3215943d28af


#### HTML Reports
<details>
<summary>Click to expand instructions</summary>

1. Browse to the project Reports folder and choose the report ,you can drag and drop it to any browser to view it.

2. The HTML report name represent the date & time of the run.

3. The report include all the run data for each test case and their status

4. Upon failure the report will include the screenshot when it failed and the specific error logs
</details> 

#### Jenkins Reports 
<details>
<summary>Click to expand instructions</summary>

1. Access Jenkins: Open your Jenkins instance and navigate to the project for which the tests were executed.

2. View Report in Jenkins:
 - Locate the “Build History” section and select the specific build you want to analyze.
 - Inside the build details, you can find links to test reports, typically labeled as “Test Results” or under “HTML Publisher Plugin” if configured.
3. Detailed Test Analysis: The Jenkins report displays test statuses, including any test failures, along with logs. You’ll also see an option to view error screenshots and logs for failed tests if configured to save these artifacts.
4. Trend Analysis: Jenkins provides a view of historical test data, helping track trends in test pass/fail rates over time, enabling insights into project quality and stability.

</details>   

![image](https://github.com/user-attachments/assets/14e6db20-42f4-4823-a63d-b67cf055fb84)

#### Allure Reports 
<details>
<summary>Click to expand instructions</summary>

#### How to Use Allure Reports on Windows

1. **Run the Script from the Project Root**  
   To generate the Allure report, run the attached PowerShell script from the project root folder using the following command:
   ```powershell
   .\allure_run_ps1
   ```
   If you're familiar with the script and know what you're doing, you can edit the run parameters directly within the PowerShell script.
2. **View the report**  
   At the end of the run, the report will automatically open in your default web browser.
3. **Manually generate the report**  
   If you want to manually generate the report, use the following command:
   ```powershell
   allure serve PATH_TO_REPORT
   ```
Advise : The Allure report keeps a history of test runs, allowing you to view results for each run. Each new test run will be stored and can be reviewed as part of the history.

For more info:
- [Allure Pytest Integration](https://allurereport.org/docs/pytest/)
- [Allure Report Generation Docs](https://allurereport.org/docs/) 
</details> 

![Allure ](https://github.com/user-attachments/assets/2f277021-6151-4a44-b198-813cac386873)

## 🚀 Planned Enhancements

Future updates will aim to extend the functionality and robustness of this framework, with potential additions including:

- Enhanced reporting capabilities using allure reports was **integrated to the tests** (Details will follow)
- Detailed README updates, including Docker command instructions ,setting up Jenkins job/pipeline and example screenshots for a clearer demo experience
- Demonstration of API testing and backend database integration will be introduced in another public project (Link to the project will be added here)

## Contributing

This project is designed for demonstration purposes and is currently set as read-only for showcasing the framework’s capabilities. Contributions are not open at this time, but feel free to explore and use the code as a reference for similar projects.

