# 🤖 EasyQA AI Testing Framework - Complete Guide

## 🌟 Overview

EasyQA is a next-generation, AI-powered test automation framework that combines the best of traditional testing frameworks with cutting-edge machine learning capabilities. It supports both Java and Python, offering a comprehensive solution for modern test automation needs.

### Why EasyQA AI Framework?

- **🧠 AI-Powered Testing**: Self-healing locators, visual regression with ML, predictive analytics
- **🔄 Multi-Language Support**: Java (Selenium + TestNG) and Python (Playwright + pytest)
- **📊 Intelligent Insights**: ML-driven failure prediction and test analytics
- **🎨 Visual Testing**: Computer vision-based visual regression testing
- **🚀 Modern Tools**: Playwright, Selenium 4, TestNG 7, pytest
- **📈 Comprehensive Reporting**: Allure, ExtentReports, custom AI insights
- **🐳 Containerized**: Full Docker support with docker-compose
- **⚡ Performance Testing**: Built-in Lighthouse integration and performance metrics
- **♿ Accessibility**: Automated accessibility testing with axe-core

## 🏗️ Architecture

```
EasyQA Framework
├── Java Layer (Selenium + TestNG)
│   ├── Page Object Model
│   ├── API Testing (REST Assured)
│   ├── Data-Driven Testing
│   └── Parallel Execution
│
├── Python Layer (Playwright + AI)
│   ├── AI Visual Testing
│   ├── Self-Healing Locators
│   ├── ML Analytics
│   ├── Test Data Generation
│   └── Performance Testing
│
├── AI/ML Features
│   ├── Visual Regression (OpenCV, scikit-image)
│   ├── Failure Prediction (Random Forest)
│   ├── Element Detection (Computer Vision)
│   └── Test Data Generation (Faker + ML)
│
└── Reporting & Analytics
    ├── Allure Reports
    ├── ExtentReports
    ├── ML Insights Dashboard
    └── Visual Diff Reports
```

## 🚀 Quick Start

### Prerequisites

- **Java**: JDK 11+
- **Python**: 3.9+
- **Maven**: 3.6+
- **Docker** (optional)
- **Git**

### Installation

#### Option 1: Local Installation

```bash
# Clone the repository
git clone https://github.com/anil-babu/EasyQA-Framework.git
cd EasyQA-Framework

# Install Java dependencies
mvn clean install -DskipTests

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

#### Option 2: Docker

```bash
# Build and run with Docker
docker build -t easyqa-framework .
docker run --rm easyqa-framework

# Or use docker-compose for full stack
docker-compose up
```

### Running Tests

#### Java Tests (Selenium)

```bash
# Run all Java tests
mvn test

# Run with specific browser
mvn test -Dbrowser=chrome

# Run specific test class
mvn test -Dtest=LoginTests

# Generate reports
mvn allure:serve
```

#### Python Tests (Playwright + AI)

```bash
# Run all Python tests
pytest python/easyqa/tests/ -v

# Run with specific browser
EASYQA_BROWSER=firefox pytest python/easyqa/tests/ -v

# Run example e-commerce tests
pytest python/easyqa/tests/examples/test_ecommerce_demo.py -v -s

# Generate HTML report
pytest python/easyqa/tests/ --html=report.html --self-contained-html
```

## 🤖 AI Features

### 1. Visual Regression Testing

AI-powered visual testing using computer vision and multiple comparison algorithms.

```python
from easyqa.visual.visual_tester import VisualTester

# Initialize visual tester
visual_tester = VisualTester(threshold=0.95)

# Capture baseline
visual_tester.capture_baseline('screenshot.png', 'homepage')

# Compare with current
result = visual_tester.compare_images(
    'baseline.png',
    'current.png',
    'homepage'
)

# Get AI insights
insights = visual_tester.get_ai_insights(result)
print(insights)
```

**Features:**
- ✅ Structural Similarity Index (SSIM)
- ✅ Perceptual hashing
- ✅ Pixel-by-pixel comparison
- ✅ Feature matching (ORB algorithm)
- ✅ Visual difference highlighting

### 2. Self-Healing Locators

ML-powered element location that automatically fixes broken locators.

```python
from easyqa.locators.self_healing import SelfHealingLocator
from selenium.webdriver.common.by import By

# Initialize self-healing locator
healer = SelfHealingLocator(confidence_threshold=0.8)

# Find element with auto-healing
element, metadata = healer.find_element(
    driver,
    By.ID,
    'old-button-id',
    context={'page': 'login', 'role': 'submit'}
)

if metadata['healed']:
    print(f"✨ Locator healed! Confidence: {metadata['confidence']}")
    print(f"New locator: {metadata['healed_by']}={metadata['healed_value']}")

# Get healing statistics
stats = healer.get_healing_stats()
print(f"Success rate: {stats['success_rate']}%")
```

**Features:**
- ✅ Automatic locator repair
- ✅ ML-based element matching
- ✅ Historical learning
- ✅ Context-aware healing
- ✅ Confidence scoring

### 3. ML-Powered Analytics

Predictive test analytics using machine learning.

```python
from easyqa.analytics.ml_analytics import MLAnalytics

# Initialize analytics
analytics = MLAnalytics()

# Record test results (happens automatically)
analytics.record_test_result({
    'name': 'test_login',
    'status': 'passed',
    'execution_time': 2.5,
    'browser': 'chrome',
    'step_count': 5
})

# Predict test failure
prediction = analytics.predict_test_failure({
    'name': 'test_checkout',
    'browser': 'chrome',
    'step_count': 12,
    'priority': 'critical'
})

print(f"Prediction: {prediction['prediction']}")
print(f"Probability: {prediction['probability']}")
print(f"Confidence: {prediction['confidence']}")

# Get comprehensive insights
insights = analytics.generate_test_insights()
print(insights['recommendations'])
```

**Features:**
- ✅ Failure prediction
- ✅ Flaky test detection
- ✅ Pattern analysis
- ✅ Trend analysis
- ✅ Smart recommendations

### 4. AI Test Data Generation

Intelligent test data generation using Faker and ML patterns.

```python
from easyqa.data_generation.ai_data_generator import AIDataGenerator

# Initialize generator
data_gen = AIDataGenerator(locale='en_US', seed=42)

# Generate user profiles
users = data_gen.generate_user_profile(count=10)

# Generate e-commerce data
ecommerce_data = data_gen.generate_ecommerce_data(
    product_count=50,
    order_count=20
)

# Generate form data
contact_form = data_gen.generate_form_data('contact')
registration_form = data_gen.generate_form_data('registration')

# Generate edge cases
edge_cases = data_gen.generate_edge_cases('email')

# Custom dataset from schema
schema = {
    'name': {'type': 'name'},
    'email': {'type': 'email'},
    'age': {'type': 'integer', 'min': 18, 'max': 65}
}
dataset = data_gen.generate_dataset(schema, count=100)
```

### 5. Playwright AI Wrapper

Enhanced Playwright with AI capabilities.

```python
from easyqa.integrations.playwright_wrapper import PlaywrightAI

async def test_with_ai():
    async with PlaywrightAI(browser_type='chromium') as browser:
        # Navigate with performance tracking
        await browser.navigate('https://example.com')

        # AI-enhanced interactions
        await browser.ai_click('#submit-button')
        await browser.ai_fill('#email', 'test@example.com')

        # Smart waiting
        await browser.smart_wait_for_element('.success-message')

        # AI data extraction
        data = await browser.ai_extract_data({
            'title': {'selector': 'h1', 'type': 'text'},
            'products': {'selector': '.product', 'type': 'list'}
        })

        # Performance audit
        performance = await browser.run_lighthouse_audit()

        # Accessibility check
        violations = await browser.get_accessibility_violations()

        # Network summary
        network = await browser.get_network_summary()
```

**Features:**
- ✅ Auto-waiting and retry logic
- ✅ Performance monitoring
- ✅ Accessibility testing
- ✅ Network activity tracking
- ✅ Video recording
- ✅ HAR file generation

## 📊 Reporting

### Allure Reports (Java)

```bash
# Generate and serve Allure report
mvn allure:serve

# Generate report only
mvn allure:report
```

### ExtentReports (Java)

Reports are automatically generated in `test-output/reports/extent-report.html`

### Pytest HTML Reports (Python)

```bash
pytest --html=report.html --self-contained-html
```

### AI Insights Dashboard

Visual and ML insights are saved in:
- `visual_results/` - Visual comparison results
- `data/test_history.json` - ML analytics data
- `logs/` - Execution logs with AI insights

## 🐳 Docker Usage

### Single Container

```bash
# Build image
docker build -t easyqa-framework .

# Run tests
docker run --rm \
  -v $(pwd)/test-output:/app/test-output \
  easyqa-framework

# Run specific tests
docker run --rm easyqa-framework pytest python/easyqa/tests/ -v
```

### Docker Compose (Selenium Grid)

```bash
# Start entire test infrastructure
docker-compose up

# Run tests on grid
docker-compose up easyqa-tests

# View Allure reports
# Open http://localhost:5050

# View Selenium Grid
# Open http://localhost:4444
```

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
browser:
  default: chrome
  headless: false

ai:
  visual_testing:
    enabled: true
    threshold: 0.95

  self_healing:
    enabled: true
    confidence_threshold: 0.8

reporting:
  screenshots_on_failure: true
  ai_insights: true

performance:
  lighthouse_enabled: true
  load_time_threshold: 3.0
```

## 📚 Examples

### Complete E-commerce Test Example

```python
import pytest
from easyqa.integrations.playwright_wrapper import PlaywrightAI
from easyqa.visual.visual_tester import VisualTester
from easyqa.data_generation.ai_data_generator import AIDataGenerator

@pytest.mark.asyncio
async def test_complete_ecommerce_flow():
    """Complete e-commerce flow with AI features."""

    # Initialize components
    browser = PlaywrightAI(browser_type='chromium')
    await browser.start()

    visual_tester = VisualTester()
    data_gen = AIDataGenerator()

    # Navigate and capture baseline
    await browser.navigate('https://demo-ecommerce.com')
    screenshot = await browser.capture_screenshot()

    # Visual regression test
    if baseline_exists:
        result = visual_tester.compare_images(baseline, screenshot, 'homepage')
        assert result['passed'], "Visual regression detected!"

    # Generate test data
    user_data = data_gen.generate_user_profile()

    # Perform actions
    await browser.ai_fill('#email', user_data['email'])
    await browser.ai_click('.login-button')

    # Check performance
    performance = await browser.get_performance_metrics()
    assert performance['loadComplete'] < 3000, "Page load too slow!"

    # Check accessibility
    violations = await browser.get_accessibility_violations()
    critical = [v for v in violations if v['impact'] == 'critical']
    assert len(critical) == 0, "Critical accessibility issues found!"

    await browser.close()
```

## 🧪 Best Practices

1. **Use AI Visual Testing for UI Stability**
   - Capture baselines for critical pages
   - Run visual regression on every deployment

2. **Enable Self-Healing in CI/CD**
   - Reduces maintenance overhead
   - Automatically adapts to minor UI changes

3. **Leverage ML Analytics**
   - Predict which tests might fail
   - Identify and fix flaky tests
   - Optimize test execution order

4. **Generate Realistic Test Data**
   - Use AI data generator for forms
   - Include edge cases in test suites

5. **Monitor Performance**
   - Track page load times
   - Set performance budgets
   - Use Lighthouse audits

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Selenium** - Browser automation
- **Playwright** - Modern browser automation
- **TestNG** - Test orchestration
- **pytest** - Python testing framework
- **OpenCV** - Computer vision
- **scikit-learn** - Machine learning
- **Faker** - Test data generation
- **Allure** - Test reporting

## 📧 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/anil-babu/EasyQA-Framework/issues)
- Documentation: [Wiki](https://github.com/anil-babu/EasyQA-Framework/wiki)

---

**Made with ❤️ by the EasyQA Team**

*Empowering QA engineers with AI-powered testing*
