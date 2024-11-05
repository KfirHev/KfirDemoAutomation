# Use the official Python image as a base
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install tzdata and venv, and create a virtual environment
RUN apt-get update && apt-get install -y tzdata python3-venv && \
    # Set the time zone to Israel
    ln -fs /usr/share/zoneinfo/Asia/Jerusalem /etc/localtime && \
    echo "Asia/Jerusalem" > /etc/timezone && \
    # Create the virtual environment
    python3 -m venv /venv

# Ensure the virtual environment is activated and install project dependencies
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Set the PATH to include the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy the rest of the application code into the container
COPY . .

# Command to run tests
CMD ["pytest", "--maxfail=1", "--disable-warnings", "-v", "--html=Reports/report.html"]
