# EasyQA Framework

## Overview

**EasyQA** is a next-generation, AI-powered test automation framework that combines the robustness of Java/Selenium with cutting-edge AI/ML capabilities. Built using enterprise-level design patterns, it provides both traditional automation (Page Object Model, API testing) and advanced AI features (visual regression testing, self-healing locators, predictive analytics).

This framework aims to provide a complete, production-ready solution for modern test automation, emphasizing:
- 🤖 **AI-Powered Testing** - Visual regression, self-healing locators, ML analytics
- 🎯 **Enterprise Quality** - Clean code, design patterns, comprehensive reporting
- 🚀 **Developer Experience** - Easy setup, detailed documentation, CI/CD ready
- 🔧 **Flexibility** - Java + Python, Selenium + Playwright, traditional + AI testing

## ✨ Features

### 🤖 AI/ML-Powered Capabilities
* **Visual Regression Testing:** AI-powered image comparison using SSIM, perceptual hashing, pixel diff, and feature matching (OpenCV)
* **Self-Healing Locators:** ML-based element detection that automatically fixes broken locators using similarity algorithms
* **Predictive Analytics:** Random Forest ML model to predict test failures and identify flaky tests
* **AI Test Data Generation:** Intelligent test data creation using Faker - user profiles, e-commerce data, forms, edge cases
* **Performance Testing:** Lighthouse integration for automated performance metrics collection
* **Accessibility Testing:** Built-in axe-core integration for WCAG compliance checking
* **Smart Waiting:** AI-enhanced element waiting with automatic retry and fallback mechanisms

### 🎯 Traditional Automation (Java/Selenium)
* **Page Object Model (POM):** Organizes UI elements and interactions for better maintainability and code reuse
* **WebDriver Management:** Uses `WebDriverManager` for automatic browser driver setup (Chrome, Firefox, Edge supported)
* **Cross-Browser Testing:** Easily configure and run tests across different browsers
* **Parallel Execution:** Designed with `ThreadLocal` WebDriver instances to support parallel test execution via TestNG
* **Configuration Management:** Externalized configuration using `.properties` and YAML files
* **Detailed Reporting:** Integrated with ExtentReports and Allure for comprehensive HTML test reports
* **Logging:** Uses Log4j 2 for detailed logging during test execution
* **Data-Driven Testing:** Utilities for reading test data from Excel files using Apache POI
* **API Testing Support:** REST Assured integration for API testing alongside UI tests
* **Utility Classes:** Reusable helper methods for common actions

## 🛠️ Tech Stack

### Java Layer
* **Language:** Java 11+
* **Build Tool:** Apache Maven
* **UI Automation:** Selenium WebDriver 4
* **Test Runner:** TestNG
* **API Testing:** REST Assured
* **Reporting:** ExtentReports, Allure Reports
* **Logging:** Log4j 2
* **Driver Management:** WebDriverManager (io.github.bonigarcia)
* **Data Handling:** Apache POI (Excel), Jackson (JSON)

### Python AI/ML Layer
* **Language:** Python 3.9-3.11
* **Browser Automation:** Playwright 1.41+
* **ML Framework:** scikit-learn (Random Forest, predictive models)
* **Computer Vision:** OpenCV (opencv-python-headless)
* **Image Processing:** Pillow, imagehash, SSIM
* **Test Data:** Faker (intelligent data generation)
* **Data Analysis:** pandas, numpy
* **Testing:** pytest, pytest-asyncio
* **Configuration:** PyYAML, python-dotenv

### Infrastructure & DevOps
* **Containerization:** Docker, Docker Compose
* **CI/CD:** GitHub Actions (with v4 actions)
* **Browser Grid:** Selenium Grid (optional)
* **Version Control:** Git

## 📂 Project Structure

```
EasyQA-Framework/
├── 📄 pom.xml                      # Maven configuration
├── 📄 setup.py                     # Python package setup
├── 📄 requirements-minimal.txt     # Minimal Python dependencies (recommended)
├── 📄 requirements.txt             # Full Python dependencies
│
├── 🔧 Docker & CI/CD
│   ├── Dockerfile                  # Full Docker image
│   ├── Dockerfile.lightweight      # Fast Docker image (recommended)
│   ├── docker-compose.yml          # Full stack with Selenium Grid
│   ├── docker-compose.lightweight.yml
│   └── .github/workflows/
│       ├── ci-simplified.yml       # Active CI/CD workflow
│       └── maven.yml               # Maven build workflow
│
├── 📚 Java Layer (src/)
│   ├── main/java/com/anil/qa/
│   │   ├── base/                   # BaseTest, BasePage, DriverManager
│   │   ├── config/                 # Configuration classes
│   │   ├── pages/                  # Page Object Model classes
│   │   ├── utils/                  # ConfigManager, ReportManager, ExcelUtils
│   │   └── constants/              # Project constants
│   └── test/java/com/anil/qa/
│       └── tests/                  # TestNG test classes
│
├── 🤖 Python AI/ML Layer (python/)
│   └── easyqa/
│       ├── core/
│       │   └── config.py           # Configuration management
│       ├── visual/
│       │   └── visual_tester.py    # AI visual regression testing
│       ├── locators/
│       │   └── self_healing.py     # ML-powered self-healing locators
│       ├── analytics/
│       │   └── ml_analytics.py     # ML predictive analytics
│       ├── data_generation/
│       │   └── ai_data_generator.py # AI test data generation
│       ├── integrations/
│       │   └── playwright_wrapper.py # Enhanced Playwright
│       ├── tests/
│       │   ├── test_unit.py        # Unit tests (19 tests)
│       │   └── examples/           # Example test suites
│       └── cli.py                  # Command-line interface
│
├── 📖 Documentation
│   ├── README.md                   # This file
│   ├── README_AI.md                # Detailed AI features guide
│   ├── INSTALL.md                  # Installation guide
│   ├── DEPENDENCY_FIX.md           # Dependency troubleshooting
│   ├── DOCKER.md                   # Docker documentation
│   ├── CI_CD_SETUP.md              # CI/CD guide
│   └── FIXES_SUMMARY.md            # Comprehensive fixes summary
│
└── 🗂️ Test Output
    ├── test-output/                # TestNG/Maven reports
    ├── allure-results/             # Allure test results
    ├── screenshots/                # Test screenshots
    └── visual-baselines/           # Visual regression baselines
```
## 🚀 Getting Started

### Prerequisites

**For Java Layer:**
* Java Development Kit (JDK) 11 or higher
* Apache Maven 3.6+
* Git

**For Python AI/ML Layer:**
* Python 3.9, 3.10, or 3.11
* pip (Python package manager)

**Optional:**
* Docker & Docker Compose (for containerized testing)
* IDE: IntelliJ IDEA, VS Code, or PyCharm

### Quick Start (3 Options)

#### Option 1: Minimal Python Setup (Recommended - 2-3 min)

```bash
# Clone the repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install minimal Python dependencies (~200MB, 2-3 min)
pip install -r requirements-minimal.txt

# Install Playwright browsers
playwright install chromium firefox

# Run Python unit tests (19 tests, ~4 seconds)
python -m pytest python/easyqa/tests/test_unit.py -v
```

#### Option 2: Java Setup

```bash
# Clone the repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Build with Maven
mvn clean install -DskipTests

# Run Java tests
mvn clean test
```

#### Option 3: Docker Setup (5 min build)

```bash
# Clone the repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Build and run with lightweight Docker image
docker build -f Dockerfile.lightweight -t easyqa-framework:light .
docker run --rm easyqa-framework:light

# Or use helper script
chmod +x docker-build-and-run.sh
./docker-build-and-run.sh lightweight
```

### Configuration

**Java Configuration:** `src/main/resources/config.properties`
* `url` - Base URL of application under test
* `browser` - Default browser (chrome, firefox, edge)
* `headless` - Run browsers in headless mode (true/false)

**Python Configuration:** `config/config.yaml`
* Visual testing thresholds
* Self-healing locator confidence levels
* ML analytics settings
* Playwright browser options

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

## ▶️ Running Tests

### Python AI/ML Tests

```bash
# Run all unit tests (19 tests, ~4 seconds)
python -m pytest python/easyqa/tests/test_unit.py -v

# Run specific test class
python -m pytest python/easyqa/tests/test_unit.py::TestDataGenerator -v

# Run with coverage
python -m pytest python/easyqa/tests/test_unit.py --cov=easyqa --cov-report=html

# Run example e-commerce tests (requires external site)
python -m pytest python/easyqa/tests/examples/test_ecommerce_demo.py -v
```

### Java/Selenium Tests

```bash
# Run all tests with Maven
mvn clean test

# Run specific test suite
mvn test -Dsurefire.suiteXmlFiles=src/test/resources/your_suite.xml

# Run specific test class
mvn test -Dtest=YourTestClass

# Run with specific browser
mvn test -Dbrowser=chrome

# Run in parallel
mvn test -DthreadCount=3
```

### Using IDE

**TestNG (Java):**
* Right-click `testng.xml` → "Run as TestNG Suite"
* Right-click test class/method → "Run as TestNG Test"

**pytest (Python):**
* Right-click test file → "Run pytest in test_unit.py"
* Use IDE's built-in test runner for individual tests

### Docker Tests

```bash
# Run tests in Docker
docker run --rm easyqa-framework:light python -m pytest python/easyqa/tests/test_unit.py -v

# Run with volume mount for reports
docker run --rm -v $(pwd)/test-output:/app/test-output easyqa-framework:light
```

## 📊 Reporting

### Java Test Reports
* **ExtentReports:** HTML reports in `test-output/reports/` with screenshots embedded
* **Allure Reports:** Generate with `mvn allure:report`, view with `mvn allure:serve`
* **TestNG Reports:** Default reports in `test-output/` directory
* **Screenshots:** Auto-captured on failure in `test-output/screenshots/`
* **Logs:** Log4j 2 console and file logging

### Python Test Reports
* **pytest HTML:** Generate with `pytest --html=report.html`
* **Coverage Reports:** Generate with `pytest --cov=easyqa --cov-report=html`
* **Visual Regression:** Comparison images saved in `visual-baselines/`
* **ML Analytics:** Test insights and predictions in JSON format
* **Console Output:** Detailed test execution logs with timing

### CI/CD Reports
* **GitHub Actions Artifacts:** Download test reports and screenshots from workflow runs
* **Status Badges:** Build status visible in repository
* **Allure Integration:** Historical test trends and failure analysis

## 🤝 Contributing (Optional)

Contributions, issues, and feature requests are welcome. If you plan to contribute, please fork the repository and create a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔄 CI/CD

### GitHub Actions Workflows

**ci-simplified.yml** (Active - Runs on every push)
* ✅ **Quick Build:** Import checks and syntax validation (~1 min)
* ✅ **Python Unit Tests:** All 19 unit tests with proper environment (~2 min)
* ✅ **Code Quality:** Black formatter validation
* ✅ **Docker Build:** Optional lightweight Docker image build
* ✅ **Total Runtime:** 5-10 minutes
* ✅ **Uses Latest Actions:** All GitHub Actions updated to v4 (April 2024+)

**maven.yml** (Java CI/CD)
* ✅ **Java Build:** Maven clean test with JDK 11
* ✅ **Allure Reports:** Generated and uploaded as artifacts
* ✅ **Caching:** Maven dependencies cached for faster builds
* ✅ **Updated Actions:** All actions upgraded to v4

### Recent CI/CD Fixes Applied
1. ✅ Updated `actions/upload-artifact` from v3 → v4 (deprecated warning fixed)
2. ✅ Updated `actions/checkout`, `actions/setup-java`, `actions/cache` to v4
3. ✅ Fixed Python module imports with `python -m pytest`
4. ✅ Added `pythonpath = python` to pytest.ini
5. ✅ Created lightweight, reliable unit tests (no external dependencies)

### Viewing CI/CD Results
```bash
# Download artifacts from GitHub Actions
# Navigate to Actions tab → Select workflow run → Download artifacts

# View Allure report locally
allure serve allure-results/
```

## 🐳 Docker

### Quick Docker Commands

```bash
# Lightweight build (recommended - 5 min, 1.5GB)
docker build -f Dockerfile.lightweight -t easyqa-framework:light .
docker run --rm easyqa-framework:light

# Full build with all features
docker build -t easyqa-framework .
docker run --rm easyqa-framework

# Docker Compose with Selenium Grid
docker-compose -f docker-compose.lightweight.yml up

# Helper script
chmod +x docker-build-and-run.sh
./docker-build-and-run.sh lightweight
```

See [DOCKER.md](DOCKER.md) for detailed Docker documentation and troubleshooting.

## 🤖 AI Features Usage

### Visual Regression Testing

```python
from easyqa.visual.visual_tester import VisualTester

tester = VisualTester()
result = tester.compare_images("baseline.png", "current.png", "homepage")
# Returns: SSIM score, perceptual hash, pixel diff, feature matching
```

### Self-Healing Locators

```python
from easyqa.locators.self_healing import SelfHealingLocator
from selenium.webdriver.common.by import By

healer = SelfHealingLocator()
element, metadata = healer.find_element(driver, By.ID, "old-id")
# Automatically finds similar elements if locator fails
```

### ML Analytics & Predictions

```python
from easyqa.analytics.ml_analytics import MLAnalytics

analytics = MLAnalytics()
analytics.record_result("test_login", "passed", duration=2.5)
prediction = analytics.predict_test_failure({"duration": 5.2, "retry_count": 2})
# Predicts: likely to fail, flaky test, or stable
```

### AI Test Data Generation

```python
from easyqa.data_generation.ai_data_generator import AIDataGenerator

generator = AIDataGenerator()
user = generator.generate_user_profile()
ecommerce = generator.generate_ecommerce_data(product_count=10)
form_data = generator.generate_form_data("registration")
```

See [README_AI.md](README_AI.md) for comprehensive AI features documentation.

## 📚 Documentation

* **[README_AI.md](README_AI.md)** - Complete AI features guide with examples
* **[INSTALL.md](INSTALL.md)** - Detailed installation instructions
* **[DOCKER.md](DOCKER.md)** - Docker setup and troubleshooting
* **[CI_CD_SETUP.md](CI_CD_SETUP.md)** - CI/CD configuration guide
* **[FIXES_SUMMARY.md](FIXES_SUMMARY.md)** - All fixes applied to the framework
* **[DEPENDENCY_FIX.md](DEPENDENCY_FIX.md)** - Dependency troubleshooting

## ✅ Test Results

### Current Status
* ✅ **19/19 Python unit tests passing** (4.18 seconds)
* ✅ **All CI/CD checks passing**
* ✅ **GitHub Actions updated to v4**
* ✅ **Zero external dependencies in unit tests**
* ✅ **Production-ready framework**

### Test Coverage
* **TestDataGenerator:** 6 tests ✅
* **TestMLAnalytics:** 4 tests ✅
* **TestConfig:** 4 tests ✅
* **TestVisualTester:** 2 tests ✅
* **TestSelfHealing:** 3 tests ✅

## 🔧 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'easyqa'**
```bash
# Solution 1: Use python -m pytest instead of pytest
python -m pytest python/easyqa/tests/test_unit.py -v

# Solution 2: Set PYTHONPATH
export PYTHONPATH=/path/to/EasyQA-Framework/python
pytest python/easyqa/tests/test_unit.py -v
```

**Dependency Installation Failures**
```bash
# Use minimal requirements (recommended)
pip install -r requirements-minimal.txt

# See DEPENDENCY_FIX.md for detailed troubleshooting
```

**Docker Build Failures**
```bash
# Use lightweight Dockerfile (faster, more reliable)
docker build -f Dockerfile.lightweight -t easyqa-framework:light .

# See DOCKER.md for detailed troubleshooting
```

**GitHub Actions Deprecated Warnings**
* ✅ Fixed! All actions updated to v4 in latest commit
* `actions/upload-artifact@v3` → `@v4`
* `actions/checkout@v3` → `@v4`
* `actions/setup-java@v3` → `@v4`

## 🎯 Key Highlights

### What Makes This Framework Special?

1. **🤖 AI-First Design**
   - Only open-source framework combining traditional + AI testing
   - Computer vision for visual regression (4 algorithms)
   - ML-powered failure prediction and flaky test detection
   - Self-healing locators that adapt to UI changes

2. **⚡ Production-Ready**
   - 19/19 tests passing with zero flakiness
   - Complete CI/CD with GitHub Actions
   - Docker support for consistent environments
   - Comprehensive documentation (7 guides)

3. **🔧 Developer-Friendly**
   - 2-3 minute setup time
   - Clear, well-documented code
   - Extensive examples and usage patterns
   - Both Java and Python support

4. **📈 Enterprise-Grade**
   - Page Object Model architecture
   - Parallel execution support
   - Multiple reporting formats
   - Configuration management
   - Proper logging and debugging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/EasyQA-Framework.git
cd EasyQA-Framework

# Install dependencies
pip install -r requirements-minimal.txt
mvn clean install -DskipTests

# Run tests to verify
python -m pytest python/easyqa/tests/test_unit.py -v
mvn clean test

# Format code
black python/
mvn formatter:format
```

## 📞 Support

- **Issues:** Report bugs or request features via [GitHub Issues](https://github.com/anil-babu/EasyQA-Framework/issues)
- **Documentation:** Check the [docs folder](.) for comprehensive guides
- **Examples:** See `python/easyqa/tests/examples/` for usage examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Built with open-source technologies:
- Selenium WebDriver, Playwright
- scikit-learn, OpenCV, pandas
- TestNG, pytest
- Maven, Docker
- GitHub Actions

---

**Built with ❤️ for the testing community**

*EasyQA Framework - Where Traditional Testing Meets AI Innovation*
