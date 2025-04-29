package com.anil.qa.base;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxOptions;
import org.openqa.selenium.safari.SafariDriver;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import com.anil.qa.utils.ConfigManager;

public class DriverManager {
    private static final Logger logger = LogManager.getLogger(DriverManager.class);
    private static final ThreadLocal<WebDriver> driver = new ThreadLocal<>();
    
    private DriverManager() {
        // Private constructor to prevent instantiation
    }
    
    public static WebDriver getDriver() {
        if (driver.get() == null) {
            setupDriver();
        }
        return driver.get();
    }
    
    public static void setupDriver() {
        String browser = ConfigManager.getProperty("browser").toLowerCase();
        boolean headless = Boolean.parseBoolean(ConfigManager.getProperty("headless"));
        
        logger.info("Setting up {} browser", browser);
        
        switch (browser) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                if (headless) {
                    chromeOptions.addArguments("--headless");
                }
                chromeOptions.addArguments("--no-sandbox");
                chromeOptions.addArguments("--disable-dev-shm-usage");
                driver.set(new ChromeDriver(chromeOptions));
                break;
                
            case "firefox":
                WebDriverManager.firefoxdriver().setup();
                FirefoxOptions firefoxOptions = new FirefoxOptions();
                if (headless) {
                    firefoxOptions.addArguments("--headless");
                }
                driver.set(new FirefoxDriver(firefoxOptions));
                break;
                
            case "edge":
                WebDriverManager.edgedriver().setup();
                driver.set(new EdgeDriver());
                break;
                
            case "safari":
                driver.set(new SafariDriver());
                break;
                
            default:
                logger.error("Unsupported browser: {}", browser);
                throw new RuntimeException("Unsupported browser: " + browser);
        }
        
        logger.info("{} browser set up successfully", browser);
        driver.get().manage().window().maximize();
    }
    
    public static void quitDriver() {
        if (driver.get() != null) {
            logger.info("Quitting WebDriver");
            driver.get().quit();
            driver.remove();
        }
    }
}