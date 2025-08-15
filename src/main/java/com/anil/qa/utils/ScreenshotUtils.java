package com.anil.qa.utils;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.commons.io.FileUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

/**
 * ScreenshotUtils provides static methods to capture and save screenshots during test execution.
 */
public class ScreenshotUtils {
    private static final Logger logger = LogManager.getLogger(ScreenshotUtils.class);
    
    private ScreenshotUtils() {
        // Private constructor to prevent instantiation
    }
    
    /**
     * Captures a screenshot and saves it to the screenshots directory.
     * @param driver the WebDriver instance
     * @param testName the name of the test
     * @return the path to the saved screenshot
     */
    public static String captureScreenshot(WebDriver driver, String testName) {
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String screenshotName = testName + "_" + timestamp + ".png";
        String screenshotDir = "test-output/screenshots";
        String screenshotPath = screenshotDir + "/" + screenshotName;
        
        try {
            File directory = new File(screenshotDir);
            if (!directory.exists()) {
                directory.mkdirs();
            }
            
            File screenshotFile = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
            File destinationFile = new File(screenshotPath);
            FileUtils.copyFile(screenshotFile, destinationFile);
            
            logger.info("Screenshot captured: {}", screenshotPath);
            return screenshotPath;
        } catch (IOException e) {
            logger.error("Failed to capture screenshot", e);
            return null;
        }
    }
}