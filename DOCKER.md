# Docker Setup Guide for EasyQA Framework

## 🐳 Docker Options

We provide multiple Docker configurations for different use cases:

### 1. Lightweight Docker (Recommended for CI/CD)

**Best for**: Quick testing, CI/CD pipelines, minimal resource usage

```bash
# Build
docker build -f Dockerfile.lightweight -t easyqa-framework:light .

# Run
docker run --rm \
  -v $(pwd)/test-output:/app/test-output \
  -v $(pwd)/screenshots:/app/screenshots \
  easyqa-framework:light
```

**Features:**
- ✅ Based on official Playwright image
- ✅ Minimal dependencies
- ✅ Fast build (~5 minutes)
- ✅ Smaller image size (~1.5GB)
- ✅ Python tests with Playwright

### 2. Full Docker

**Best for**: Complete testing with both Java and Python, Selenium support

```bash
# Build
docker build -t easyqa-framework:latest .

# Run
docker run --rm \
  -v $(pwd)/test-output:/app/test-output \
  -v $(pwd)/screenshots:/app/screenshots \
  -v $(pwd)/logs:/app/logs \
  easyqa-framework:latest
```

**Features:**
- ✅ Both Java (Selenium) and Python (Playwright)
- ✅ All AI/ML features
- ✅ Complete test suite
- ✅ Build time: ~10-15 minutes
- ✅ Image size: ~2.5GB

### 3. Docker Compose - Full Stack

**Best for**: Distributed testing with Selenium Grid

```bash
# Start entire stack
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Includes:**
- ✅ Selenium Hub
- ✅ Chrome, Firefox, Edge nodes
- ✅ Allure Report Server (http://localhost:5050)
- ✅ Test execution service
- ✅ Parallel test execution

### 4. Docker Compose - Lightweight

**Best for**: Quick testing with minimal setup

```bash
docker-compose -f docker-compose.lightweight.yml up
```

**Includes:**
- ✅ Selenium Hub
- ✅ Chrome node only
- ✅ Test execution service
- ✅ Faster startup

## 🚀 Quick Start Scripts

### Using the helper script:

```bash
# Make executable (first time only)
chmod +x docker-build-and-run.sh

# Lightweight build (default)
./docker-build-and-run.sh

# Full build
./docker-build-and-run.sh full

# Docker Compose (full)
./docker-build-and-run.sh compose

# Docker Compose (lightweight)
./docker-build-and-run.sh compose-light
```

## 📋 Dockerfile Comparison

| Feature | Lightweight | Full |
|---------|------------|------|
| Base Image | playwright/python | ubuntu:22.04 |
| Java Support | ✅ | ✅ |
| Python Support | ✅ | ✅ |
| Playwright | ✅ | ✅ |
| Selenium | ❌ | ✅ |
| Build Time | ~5 min | ~15 min |
| Image Size | ~1.5GB | ~2.5GB |
| Best For | CI/CD | Full Testing |

## 🔧 Advanced Usage

### Running Specific Tests

```bash
# Run only Python tests
docker run --rm easyqa-framework:light \
  pytest python/easyqa/tests/examples/ -v

# Run with specific markers
docker run --rm easyqa-framework:light \
  pytest -m smoke -v

# Run Java tests only (full image)
docker run --rm easyqa-framework:latest mvn test
```

### Environment Variables

```bash
docker run --rm \
  -e EASYQA_BROWSER=firefox \
  -e EASYQA_HEADLESS=true \
  -e EASYQA_AI_VISUAL=true \
  -e EASYQA_AI_HEALING=true \
  easyqa-framework:light
```

### Volume Mounts

```bash
# Mount all artifacts
docker run --rm \
  -v $(pwd)/test-output:/app/test-output \
  -v $(pwd)/screenshots:/app/screenshots \
  -v $(pwd)/videos:/app/videos \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/visual_results:/app/visual_results \
  easyqa-framework:light
```

### Interactive Shell

```bash
# Get a shell inside the container
docker run --rm -it easyqa-framework:light bash

# Then run commands
pytest python/easyqa/tests/ -v
mvn test
python python/easyqa/cli.py --help
```

## 🌐 Docker Compose Services

### Access Services

When using docker-compose, access these URLs:

- **Selenium Grid Console**: http://localhost:4444
- **Allure Reports**: http://localhost:5050
- **Allure UI**: http://localhost:5252

### Service Management

```bash
# Start specific service
docker-compose up selenium-hub chrome

# Scale nodes
docker-compose up --scale chrome=3

# Rebuild and start
docker-compose up --build

# View service logs
docker-compose logs -f easyqa-tests

# Execute in running container
docker-compose exec easyqa-tests bash
```

## 🐛 Troubleshooting

### Build Errors

**Issue**: Package installation fails

```bash
# Clean build (no cache)
docker build --no-cache -f Dockerfile.lightweight -t easyqa-framework:light .

# Check base image is available
docker pull mcr.microsoft.com/playwright/python:v1.41.0-jammy
```

**Issue**: Out of disk space

```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Runtime Errors

**Issue**: Browser not found

```bash
# Ensure browsers are installed in image
docker run --rm easyqa-framework:light playwright install --help
```

**Issue**: Permission denied on volumes

```bash
# Create directories first
mkdir -p test-output screenshots logs

# Fix permissions
chmod -R 777 test-output screenshots logs
```

**Issue**: Tests fail in Docker but work locally

```bash
# Run with same environment
docker run --rm -it \
  -e EASYQA_HEADLESS=true \
  -e CI=true \
  easyqa-framework:light bash

# Then debug
pytest python/easyqa/tests/ -v -s
```

## 📊 Performance Tips

### Faster Builds

1. **Use .dockerignore** (already configured)
2. **Layer caching**: Copy requirements before code
3. **Multi-stage builds**: Separate build and runtime
4. **Minimal base**: Use lightweight image

### Smaller Images

```bash
# Check image size
docker images | grep easyqa

# Analyze layers
docker history easyqa-framework:light

# Remove unnecessary files
docker run --rm easyqa-framework:light du -sh /app/*
```

### CI/CD Optimization

```yaml
# GitHub Actions example
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    file: Dockerfile.lightweight
    push: false
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## 🔐 Security

### Scan for Vulnerabilities

```bash
# Using Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image easyqa-framework:light

# Using Docker Scout
docker scout cves easyqa-framework:light
```

### Run as Non-Root (Advanced)

```dockerfile
# Add to Dockerfile
RUN useradd -m -u 1000 testuser && \
    chown -R testuser:testuser /app
USER testuser
```

## 📝 Docker Compose Examples

### Development Setup

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  easyqa-dev:
    build:
      context: .
      dockerfile: Dockerfile.lightweight
    volumes:
      - .:/app
      - /app/python/easyqa/__pycache__
    command: bash
    stdin_open: true
    tty: true
```

```bash
docker-compose -f docker-compose.dev.yml up
```

### Parallel Execution

```yaml
# docker-compose.parallel.yml
version: '3.8'
services:
  test-chrome:
    build: .
    environment:
      - BROWSER=chrome
  test-firefox:
    build: .
    environment:
      - BROWSER=firefox
```

## 🎯 Best Practices

1. **Use specific tags**: Don't use `latest` in production
2. **Multi-stage builds**: Separate dependencies from code
3. **Health checks**: Add HEALTHCHECK to Dockerfile
4. **Resource limits**: Set memory/CPU limits in compose
5. **Secrets management**: Use Docker secrets, not ENV vars
6. **Regular updates**: Update base images regularly

## 📚 Resources

- [Official Playwright Docker](https://playwright.dev/docs/docker)
- [Selenium Docker Images](https://github.com/SeleniumHQ/docker-selenium)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

**Need help?** Check the main [README_AI.md](README_AI.md) or open an issue on GitHub.
