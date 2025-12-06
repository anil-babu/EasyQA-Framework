# EasyQA Framework - Installation Guide

## 📋 Prerequisites

### Required
- **Java**: JDK 11 or higher
- **Maven**: 3.6+
- **Python**: 3.9, 3.10, or 3.11
- **pip**: Latest version
- **Git**: For cloning the repository

### Optional
- **Docker**: For containerized testing
- **docker-compose**: For running with Selenium Grid

## 🚀 Installation Options

### Option 1: Minimal Installation (Recommended for Quick Start)

Perfect for getting started quickly with core features.

```bash
# Clone repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install minimal Python dependencies
pip install -r requirements-minimal.txt

# Install Playwright browsers
playwright install chromium

# Install Java dependencies
mvn clean install -DskipTests
```

**What you get:**
- ✅ Playwright browser automation
- ✅ Selenium WebDriver
- ✅ Basic visual testing (OpenCV)
- ✅ Test data generation (Faker)
- ✅ Basic ML analytics (without advanced features)
- ✅ All core testing capabilities

### Option 2: Full Installation (Complete AI/ML Features)

For full ML and AI capabilities.

```bash
# Clone repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install all Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Java dependencies
mvn clean install -DskipTests
```

**What you get:**
- ✅ Everything from minimal installation
- ✅ Advanced ML predictions (Random Forest)
- ✅ Pandas-based analytics
- ✅ Enhanced reporting with visualizations
- ✅ All optional ML features

### Option 3: Docker Installation (Easiest)

No local setup required! Everything runs in Docker.

```bash
# Clone repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Build and run
docker build -t easyqa-framework .
docker run --rm easyqa-framework

# OR use docker-compose for full stack
docker-compose up
```

**What you get:**
- ✅ Complete environment
- ✅ Selenium Grid (Chrome, Firefox, Edge)
- ✅ Allure Report Server
- ✅ All dependencies pre-installed
- ✅ No local configuration needed

## 🔧 Platform-Specific Instructions

### Windows

```powershell
# Install Python from https://www.python.org/downloads/
# Install Java from https://adoptium.net/
# Install Maven from https://maven.apache.org/download.cgi

# Clone repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install Python dependencies
pip install -r requirements-minimal.txt

# Install Playwright
playwright install chromium
playwright install-deps

# Install Java dependencies
mvn clean install -DskipTests
```

### macOS

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install openjdk@11 maven python@3.11

# Clone repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install Python dependencies
pip3 install -r requirements-minimal.txt

# Install Playwright
playwright install

# Install Java dependencies
mvn clean install -DskipTests
```

### Linux (Ubuntu/Debian)

```bash
# Install prerequisites
sudo apt update
sudo apt install -y openjdk-11-jdk maven python3.11 python3-pip git

# Clone repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install Python dependencies
pip3 install -r requirements-minimal.txt

# Install Playwright
playwright install
playwright install-deps

# Install Java dependencies
mvn clean install -DskipTests
```

## 📦 Dependency Breakdown

### requirements-minimal.txt (Core Testing)
```
playwright==1.41.0          # Modern browser automation
selenium==4.16.0            # Traditional browser automation
pytest==7.4.3               # Python test framework
scikit-learn==1.3.2         # Basic ML (lightweight)
opencv-python-headless      # Visual testing
Pillow==10.2.0              # Image processing
Faker==22.0.0               # Test data generation
```

### requirements.txt (Full Stack)
All minimal dependencies PLUS:
```
pandas==2.1.4               # Advanced data analysis
matplotlib==3.8.2           # Visualization
seaborn==0.13.1             # Statistical visualization
plotly==5.18.0              # Interactive charts
sqlalchemy==2.0.25          # Database ORM
```

## 🧪 Verify Installation

Run these commands to verify everything is installed correctly:

```bash
# Check Java
java -version
# Expected: java version "11.x.x" or higher

# Check Maven
mvn -version
# Expected: Apache Maven 3.6.x or higher

# Check Python
python --version
# Expected: Python 3.9.x or 3.10.x or 3.11.x

# Run Java tests
mvn test -Dtest=LoginTests

# Run Python tests
pytest python/easyqa/tests/examples/test_ecommerce_demo.py::test_ml_predictions -v
```

## ⚠️ Common Issues & Solutions

### Issue: TensorFlow installation fails

**Solution:** TensorFlow is optional and commented out in requirements.txt. The framework works fine without it. If you need deep learning features, install separately:

```bash
pip install tensorflow
```

### Issue: Playwright browsers not installing

**Solution:**
```bash
# Run with system dependencies
playwright install-deps
playwright install
```

### Issue: numpy/scikit-learn version conflicts

**Solution:** Use the minimal requirements which have compatible versions:
```bash
pip install -r requirements-minimal.txt
```

### Issue: OpenCV import errors

**Solution:** Use headless version (already in requirements):
```bash
pip install opencv-python-headless
```

### Issue: Maven build fails

**Solution:**
```bash
# Clear Maven cache and rebuild
rm -rf ~/.m2/repository
mvn clean install -DskipTests -U
```

### Issue: Permission denied on Linux

**Solution:**
```bash
# Run Playwright install with elevated permissions
sudo playwright install-deps
```

## 🎯 Quick Start After Installation

```bash
# Run quick setup script
./quickstart.sh

# Or manually:

# 1. Run example tests
pytest python/easyqa/tests/examples/test_ecommerce_demo.py -v -s

# 2. Generate test data
python python/easyqa/cli.py generate users --count 10

# 3. Run Java tests
mvn test

# 4. View reports
mvn allure:serve
```

## 📊 Feature Availability by Installation Type

| Feature | Minimal | Full | Docker |
|---------|---------|------|--------|
| Playwright Testing | ✅ | ✅ | ✅ |
| Selenium Testing | ✅ | ✅ | ✅ |
| Visual Testing | ✅ | ✅ | ✅ |
| Self-Healing Locators | ✅ | ✅ | ✅ |
| Test Data Generation | ✅ | ✅ | ✅ |
| Basic Analytics | ✅ | ✅ | ✅ |
| ML Predictions | ⚠️ Limited | ✅ | ✅ |
| Advanced Reporting | ❌ | ✅ | ✅ |
| Selenium Grid | ❌ | ❌ | ✅ |

✅ = Fully Available
⚠️ = Limited (basic features only)
❌ = Not Available

## 🔄 Upgrading

### Update Python dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Update Java dependencies:
```bash
mvn clean install -U
```

### Update Playwright browsers:
```bash
playwright install
```

## 📚 Next Steps

After installation:
1. Read [README_AI.md](README_AI.md) for AI features guide
2. Check [examples](python/easyqa/tests/examples/) for sample tests
3. Review [configuration](config/config.yaml)
4. Run the quickstart script: `./quickstart.sh`

## 💬 Support

If you encounter issues:
- Check [Common Issues](#common-issues--solutions) above
- Open an issue on [GitHub](https://github.com/anil-babu/EasyQA-Framework/issues)
- Review documentation in README_AI.md

---

**Pro Tip:** Start with the minimal installation to get familiar with the framework, then upgrade to full installation when you need advanced ML features.
