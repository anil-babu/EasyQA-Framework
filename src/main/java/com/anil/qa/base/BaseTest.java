package com.anil.qa.base;

import java.io.IOException;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.WebDriver;
import org.testng.ITestResult;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterSuite;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.Parameters;

import com.anil.qa.utils.ConfigManager;
import com.anil.qa.utils.ReportManager;
import com.anil.qa.utils.ScreenshotUtils;

/**
 * BaseTest sets up and tears down WebDriver and reporting for all tests.
 * Handles suite and method-level setup/teardown.
 *
 * @author Anil
 * @version 1.0
 * @since 2024-01-01
 */
public class BaseTest {
    /** Logger instance. */
    private static final Logger LOGGER = LogManager.getLogger(BaseTest.class);
    /** WebDriver instance. */
    private WebDriver driver;

    /**
     * Gets the WebDriver instance.
     * @return the WebDriver
     */
    public WebDriver getDriver() {
        return driver;
    }

    /**
     * Sets the WebDriver instance.
     * @param webDriver the WebDriver to set.
     */
    public void setDriver(final WebDriver webDriver) {
        this.driver = webDriver;
    }
    
    /**
    * Runs before the test suite. Loads config and initializes reports.
     */
    @BeforeSuite
    public void beforeSuite() {
        LOGGER.info("Starting test execution");
        ConfigManager.loadConfig();
        ReportManager.initReports();
    }
    
    /**
    * Runs before each test method. Sets up WebDriver and navigates to base URL.
    * @param browser the browser to use.
     */
    @BeforeMethod
    @Parameters(value = {"browser"})
    public void beforeMethod(final String browser) {
        LOGGER.info("Setting up test method");
        if (browser != null) {
            ConfigManager.setProperty("browser", browser);
        }
        driver = DriverManager.getDriver();
        driver.get(
            ConfigManager.getProperty("url")
        );
    }
    
    /**
    * Runs after each test method. Handles reporting and driver cleanup.
    * @param result the ITestResult.
     */
    @AfterMethod
    public void afterMethod(ITestResult result) {
        if (result.getStatus() == ITestResult.FAILURE) {
            LOGGER.error("Test failed: {}", result.getName());
            String screenshotPath = ScreenshotUtils.captureScreenshot(driver, 
                    result.getName());
            ReportManager.logFailure("Test failed with exception: " 
                    + result.getThrowable().getMessage());
            try {
                ReportManager.attachScreenshot(screenshotPath);
            } catch (IOException e) {
                e.printStackTrace();
            }
        } else if (result.getStatus() == ITestResult.SUCCESS) {
            LOGGER.info("Test passed: {}", result.getName());
            ReportManager.logSuccess("Test passed successfully");
        }

        DriverManager.quitDriver();
    }

    /**
    * Runs after the test suite. Flushes reports.
     */
    @AfterSuite
    public void afterSuite() {
        LOGGER.info("Finishing test execution");
        ReportManager.flushReports();
    }
}
