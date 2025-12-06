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
    python3.11-venv \
    # Browser dependencies
    wget \
    curl \
    gnupg \
    unzip \
    # Additional tools
    git \
    vim \
    ca-certificates \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up Python alias
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3

# Upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy project files
COPY requirements-minimal.txt /app/
COPY requirements.txt /app/
COPY pom.xml /app/
COPY src /app/src/

# Install Python dependencies (minimal for faster build)
RUN pip3 install --no-cache-dir -r requirements-minimal.txt

# Install Playwright browsers with system dependencies
RUN playwright install --with-deps chromium firefox

# Install Java dependencies
RUN mvn clean install -DskipTests

# Copy remaining project files
COPY . /app/

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
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Expose ports (for potential web reporting)
EXPOSE 8080 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import playwright; import selenium" || exit 1

# Default command - run both Java and Python tests
CMD ["bash", "-c", "mvn test || true && pytest python/easyqa/tests/ -v --html=test-output/reports/pytest_report.html --self-contained-html || true"]

# Alternative commands (uncomment as needed):
# Run only Java tests
# CMD ["mvn", "test"]

# Run only Python tests
# CMD ["pytest", "python/easyqa/tests/", "-v"]

# Interactive shell
# CMD ["bash"]
