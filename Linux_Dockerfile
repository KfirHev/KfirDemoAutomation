# Use the lightweight Python 3.12 image
FROM python:3.12-slim-bookworm

# Set environment variables to avoid interactive issues
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    gnupg2 \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp/ && \
    unzip /tmp/chromedriver_linux64.zip -d /tmp/ && \
    rm /tmp/chromedriver_linux64.zip && \
    mv /tmp/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Set display port to avoid crash
#ENV DISPLAY=:99

# Copy project code
WORKDIR /app
COPY . /app

# Command to run the tests
CMD ["pytest","--run_env=docker", "--maxfail=1", "--disable-warnings", "-v" ,"--html=Reports/report.html"]

