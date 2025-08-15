package com.anil.qa.utils;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.aventstack.extentreports.ExtentReports;
import com.aventstack.extentreports.ExtentTest;
import com.aventstack.extentreports.MediaEntityBuilder;
import com.aventstack.extentreports.Status;
import com.aventstack.extentreports.reporter.ExtentSparkReporter;
import com.aventstack.extentreports.reporter.configuration.Theme;

/**
 * ReportManager handles ExtentReports initialization, logging, and screenshot attachment.
 */
public class ReportManager {
    private static final Logger logger = LogManager.getLogger(ReportManager.class);
    private static ExtentReports extentReports;
    private static ThreadLocal<ExtentTest> extentTest = new ThreadLocal<>();
    
    private ReportManager() {
        // Private constructor to prevent instantiation
    }
    
    /**
     * Initializes ExtentReports and configures the report output.
     */
    public static void initReports() {
        if (extentReports == null) {
            String timestamp = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss").format(new Date());
            String reportDir = "test-output/reports";
            String reportPath = reportDir + "/TestReport_" + timestamp + ".html";
            
            File reportDirFile = new File(reportDir);
            if (!reportDirFile.exists()) {
                reportDirFile.mkdirs();
            }
            
            extentReports = new ExtentReports();
            ExtentSparkReporter sparkReporter = new ExtentSparkReporter(reportPath);
            
            sparkReporter.config().setDocumentTitle("Automation Test Report");
            sparkReporter.config().setReportName("EasyQA Framework Report");
            sparkReporter.config().setTheme(Theme.STANDARD);
            sparkReporter.config().setTimeStampFormat("MMM dd, yyyy HH:mm:ss");
            
            extentReports.attachReporter(sparkReporter);
            extentReports.setSystemInfo("OS", System.getProperty("os.name"));
            extentReports.setSystemInfo("Java Version", System.getProperty("java.version"));
            extentReports.setSystemInfo("Browser", ConfigManager.getProperty("browser"));
            extentReports.setSystemInfo("Environment", ConfigManager.getProperty("env", "QA"));
            
            logger.info("ExtentReports initialized: {}", reportPath);
        }
    }
    
    /**
     * Creates a new test in the report.
     * @param testName the name of the test
     */
    public static void createTest(String testName) {
        ExtentTest test = extentReports.createTest(testName);
        extentTest.set(test);
        logger.info("Created test in ExtentReports: {}", testName);
    }
    
    /**
     * Logs an info message to the report.
     * @param message the message to log
     */
    public static void logInfo(String message) {
        getTest().log(Status.INFO, message);
    }
    
    /**
     * Logs a success message to the report.
     * @param message the message to log
     */
    public static void logSuccess(String message) {
        getTest().log(Status.PASS, message);
    }
    
    /**
     * Logs a failure message to the report.
     * @param message the message to log
     */
    public static void logFailure(String message) {
        getTest().log(Status.FAIL, message);
    }
    
    /**
     * Logs a warning message to the report.
     * @param message the message to log
     */
    public static void logWarning(String message) {
        getTest().log(Status.WARNING, message);
    }
    
    /**
     * Attaches a screenshot to the report.
     * @param screenshotPath the path to the screenshot
     * @throws IOException if the file cannot be read
     */
    public static void attachScreenshot(String screenshotPath) throws IOException {
        getTest().fail("Screenshot of failure", 
		        MediaEntityBuilder.createScreenCaptureFromPath(screenshotPath).build());
    }
    
    /**
     * Flushes the report output to disk.
     */
    public static void flushReports() {
        if (extentReports != null) {
            extentReports.flush();
            logger.info("ExtentReports flushed successfully");
        }
    }
    
    private static ExtentTest getTest() {
        return extentTest.get();
    }
}