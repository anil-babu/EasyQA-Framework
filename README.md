# EasyQA Framework

## Overview

EasyQA is a robust, scalable, and maintainable test automation framework built using Java, Selenium WebDriver, and TestNG. It demonstrates enterprise-level design patterns like the Page Object Model (POM) and provides a solid foundation for automating web UI and API tests.

This framework aims to provide a reusable structure for test automation projects, emphasizing clean code, configuration management, detailed reporting, and ease of use.

## ✨ Features

* **Page Object Model (POM):** Organizes UI elements and interactions for better maintainability and code reuse.
* **WebDriver Management:** Uses `WebDriverManager` for automatic browser driver setup (Chrome, Firefox, Edge supported).
* **Cross-Browser Testing:** Easily configure and run tests across different browsers.
* **Parallel Execution:** Designed with `ThreadLocal` WebDriver instances to support parallel test execution via TestNG.
* **Configuration Management:** Externalized configuration using `.properties` files for easy management of URLs, credentials, browser settings, etc.
* **Detailed Reporting:** Integrated with ExtentReports for comprehensive and visually appealing HTML test reports, including screenshots on failure.
* **Logging:** Uses Log4j 2 for detailed logging during test execution, aiding in debugging.
* **Data-Driven Testing:** Utilities included for reading test data from Excel files using Apache POI.
* **API Testing Support:** Includes utilities using REST Assured for easy integration of API tests alongside UI tests.
* **Utility Classes:** Provides reusable helper methods for common actions (screenshots, explicit waits, element interactions, API calls, etc.).

## 🛠️ Tech Stack

* **Language:** Java (JDK 11+)
* **Build Tool:** Apache Maven
* **UI Automation:** Selenium WebDriver
* **Test Runner:** TestNG
* **API Testing:** REST Assured
* **Reporting:** ExtentReports
* **Logging:** Log4j 2
* **Driver Management:** WebDriverManager (io.github.bonigarcia)
* **Data Handling:** Apache POI (for Excel)
* **JSON Handling:** Jackson Databind

## 📂 Project Structure

EasyQA-Framework/├── pom.xml                   # Maven configuration file (dependencies, plugins)├── src/│   ├── main/│   │   ├── java/│   │   │   └── com/anil/qa/  # Base package│   │   │       ├── base/     # Base classes (BaseTest, BasePage, DriverManager)│   │   │       ├── config/   # Configuration related classes (if any more complex needed)│   │   │       ├── pages/    # Page Object classes│   │   │       ├── utils/    # Utility classes (ConfigManager, ReportManager, ExcelUtils, etc.)│   │   │       └── constants/# Project constants (if needed)│   │   └── resources/        # Non-code resources for main source│   │       ├── config.properties # Framework configuration settings│   │       └── log4j2.xml    # Logging configuration│   └── test/│       ├── java/│       │   └── com/anil/qa/│       │       └── tests/    # TestNG test classes│       └── resources/        # Non-code resources for tests│           ├── testdata/│           │   └── testData.xlsx # Sample test data file│           └── testng.xml    # TestNG suite definition file├── test-output/              # Default output directory for TestNG/Maven reports│   ├── reports/              # Custom location for ExtentReports│   └── screenshots/          # Location for failure screenshots└── README.md                 # This file
## 🚀 Getting Started

### Prerequisites

* **Java Development Kit (JDK):** Version 11 or higher installed.
* **Apache Maven:** Installed and configured in your system's PATH.
* **Git:** Installed for cloning the repository.
* **An IDE (Optional but Recommended):** IntelliJ IDEA, Eclipse, or VS Code.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/EasyQA-Framework.git](https://github.com/your-username/EasyQA-Framework.git)
    cd EasyQA-Framework
    ```
    *(Replace `your-username` with your actual GitHub username)*

2.  **Build the project using Maven:**
    (This will download all dependencies defined in `pom.xml`)
    ```bash
    mvn clean install -DskipTests
    ```
    *(Using `-DskipTests` initially just builds without running tests)*

### Configuration

* Modify the `src/main/resources/config.properties` file to set:
    * `url`: The base URL of the application under test.
    * `browser`: The default browser to use (e.g., `chrome`, `firefox`, `edge`).
    * `headless`: Set to `true` to run browsers in headless mode, `false` otherwise.
    * Other environment-specific details as needed.

## ▶️ Running Tests

You can run the tests in several ways:

1.  **Using Maven:**
    * Run all tests defined in `testng.xml`:
        ```bash
        mvn clean test
        ```
    * Run specific tests or groups (configure `maven-surefire-plugin` in `pom.xml`):
        ```bash
        mvn test -Dsurefire.suiteXmlFiles=src/test/resources/your_suite.xml
        ```

2.  **Using TestNG directly (via IDE):**
    * Right-click on the `testng.xml` file in your IDE and choose "Run as TestNG Suite".
    * Right-click on a specific test class or method and choose "Run as TestNG Test".

3.  **Using `testng.xml`:**
    * Customize the `src/test/resources/testng.xml` file to define test suites, tests, classes, parameters (like browser), and parallel execution settings.

## 📊 Reporting

* **ExtentReports:** After test execution, detailed HTML reports are generated in the `test-output/reports/` directory. Open the `.html` file in a web browser to view the results.
* **Screenshots:** Screenshots for failed tests are automatically captured and saved in the `test-output/screenshots/` directory. They are also embedded within the ExtentReport.
* **Logs:** Console output will show logs based on the `log4j2.xml` configuration. Log files can also be configured if needed.

## 🤝 Contributing (Optional)

Contributions, issues, and feature requests are welcome. If you plan to contribute, please fork the repository and create a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

