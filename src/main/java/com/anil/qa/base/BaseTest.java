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

public class BaseTest {
    private static final Logger logger = LogManager.getLogger(BaseTest.class);
    protected WebDriver driver;
    
    @BeforeSuite
    public void beforeSuite() {
        logger.info("Starting test execution");
        ConfigManager.loadConfig();
        ReportManager.initReports();
    }
    
    @BeforeMethod
    @Parameters(value = {"browser"})
    public void beforeMethod(String browser) {
        logger.info("Setting up test method");
        if (browser != null) {
            ConfigManager.setProperty("browser", browser);
        }
        driver = DriverManager.getDriver();
        driver.get(ConfigManager.getProperty("url"));
    }
    
    @AfterMethod
    public void afterMethod(ITestResult result) {
        if (result.getStatus() == ITestResult.FAILURE) {
            logger.error("Test failed: {}", result.getName());
            String screenshotPath = ScreenshotUtils.captureScreenshot(driver, result.getName());
            ReportManager.logFailure("Test failed with exception: " + result.getThrowable().getMessage());
            try {
				ReportManager.attachScreenshot(screenshotPath);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
        } else if (result.getStatus() == ITestResult.SUCCESS) {
            logger.info("Test passed: {}", result.getName());
            ReportManager.logSuccess("Test passed successfully");
        }
        
        DriverManager.quitDriver();
    }
    
    @AfterSuite
    public void afterSuite() {
        logger.info("Finishing test execution");
        ReportManager.flushReports();
    }
}