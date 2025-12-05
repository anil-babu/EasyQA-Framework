# Multi-stage Dockerfile for EasyQA AI Testing Framework
# Supports both Java and Python testing

FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Java dependencies
    openjdk-11-jdk \
    maven \
    # Python dependencies
    python3.11 \
    python3-pip \
    # Browser dependencies
    wget \
    curl \
    gnupg \
    unzip \
    # Additional tools
    git \
    vim \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Firefox
RUN apt-get update \
    && apt-get install -y firefox \
    && rm -rf /var/lib/apt/lists/*

# Set up Python alias
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium firefox webkit
RUN playwright install-deps

# Install Java dependencies
RUN mvn clean install -DskipTests

# Create necessary directories
RUN mkdir -p \
    screenshots \
    videos \
    logs \
    visual_baselines \
    visual_results \
    data \
    test_data \
    models \
    test-output/reports

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV MAVEN_HOME=/usr/share/maven
ENV PATH="${JAVA_HOME}/bin:${MAVEN_HOME}/bin:${PATH}"
ENV PYTHONPATH=/app/python:${PYTHONPATH}

# Expose ports (for potential web reporting)
EXPOSE 8080 9090

# Default command - run both Java and Python tests
CMD ["bash", "-c", "mvn test && pytest python/easyqa/tests/ -v --html=test-output/reports/pytest_report.html"]

# Alternative: Run only Java tests
# CMD ["mvn", "test"]

# Alternative: Run only Python tests
# CMD ["pytest", "python/easyqa/tests/", "-v"]

# Alternative: Interactive shell
# CMD ["bash"]
