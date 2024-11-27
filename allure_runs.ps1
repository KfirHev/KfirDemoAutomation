$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Create a directory for this run
$allureResultsPath = "Reports\allure-results\$timestamp"
New-Item -ItemType Directory -Path $allureResultsPath -Force

# Set the environment variable for allure results directory
$env:ALLURE_RESULTS_PATH = $allureResultsPath

# Run tests and save results
pytest --alluredir=$allureResultsPath

# Merge history from previous runs
if (Test-Path "Reports\allure-report\history") {
    Copy-Item -Recurse -Force "Reports\allure-report\history" "$allureResultsPath\history"
}

# Generate the Allure report
allure generate $allureResultsPath --clean -o "Reports\allure-report"

# Serve the report locally
allure serve $allureResultsPath
