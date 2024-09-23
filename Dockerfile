# Use Windows Server Core as the base image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set the shell to PowerShell for the following RUN commands
SHELL ["powershell", "-Command"]


# Install Python 3.12.4
RUN Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe -OutFile python-installer.exe
RUN Start-Process -FilePath python-installer.exe -Args '/silent /install TargetDir=C:\Python' -NoNewWindow -Wait
RUN Remove-Item -Force python-installer.exe
RUN [System.Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';C:\Python', [System.EnvironmentVariableTarget]::Machine)

# Install Chrome
RUN Invoke-WebRequest -Uri https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.58/win64/chrome-win64.zip -OutFile chrome_win64.zip
RUN Expand-Archive -Path chrome_win64.zip -DestinationPath 'C:\Program Files\Chrome' -Force
RUN Remove-Item -Force chrome_win64.zip

# Install ChromeDriver (compatible with Chrome version 129.0.6668.58)
RUN Invoke-WebRequest -Uri https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/129.0.6668.58/win64/chromedriver-win64.zip -OutFile chromedriver_win64.zip
RUN Expand-Archive -Path chromedriver_win64.zip -DestinationPath 'C:\Program Files\Chrome\ChromeDriver' -Force
RUN if (Test-Path 'C:\Program Files\Chrome\ChromeDriver\chromedriver.exe') { Write-Host "ChromeDriver installed" } else { Write-Host "ChromeDriver not installed" }
RUN Remove-Item -Force chromedriver_win64.zip


# Install Firefox
#RUN Invoke-WebRequest -Uri https://download.mozilla.org/?product=firefox-stable&os=win64&lang=en-US -OutFile firefox_installer.exe
#RUN Start-Process -FilePath firefox_installer.exe -Args '/silent /install' -NoNewWindow -Wait
#RUN Remove-Item -Force firefox_installer.exe


# Set environment variables for browser drivers (assuming the drivers will be in the container's project folder)
ENV CHROMEWEBDRIVER="C:\\Program Files\\Chrome\\ChromeDriver\\chromedriver-win64\chromedriver.exe"
ENV PATH="C:\\Python;C:\\Python\\Scripts;C:\\Program Files\\Chrome\chrome-win64;C:\\Program Files\\Chrome\\ChromeDriver\\chromedriver-win64"

# Set the working directory to /app where your code will be mounted or copied
WORKDIR /app

# Copy the project files, including requirements.txt, into the container
COPY . .

# Install Python dependencies from requirements.txt
RUN ["C:\\Python\\python.exe", "-m", "pip", "install", "-r", "requirements.txt"]

#Set the default command to run tests
#CMD ["pytest", "--run_env=docker", "--maxfail=1", "--disable-warnings", "-v", "--html=Reports/report.html"]
