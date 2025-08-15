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

/**
 * DriverManager manages WebDriver instances for different browsers and threads.
 * Supports Chrome, Firefox, Edge, and Safari.
 */
public final class DriverManager {
    /** Logger instance. */
    private static final Logger LOGGER = LogManager.getLogger(DriverManager.class);
    /** ThreadLocal WebDriver instance. */
    private static final ThreadLocal<WebDriver> DRIVER = new ThreadLocal<>();

    private DriverManager() {
        // Private constructor to prevent instantiation
    }

    /**
     * Gets the current thread's WebDriver instance, creating it if necessary.
     * @return the WebDriver
     */
    public static WebDriver getDriver() {
        if (DRIVER.get() == null) {
            setupDriver();
        }
        return DRIVER.get();
    }

    /**
     * Sets up the WebDriver based on config properties.
     */
    public static void setupDriver() {
        String browser = ConfigManager.getProperty("browser").toLowerCase();
        boolean headless = Boolean.parseBoolean(
                ConfigManager.getProperty("headless"));

        LOGGER.info("Setting up {} browser", browser);

        switch (browser) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                if (headless) {
                    chromeOptions.addArguments("--headless");
                }
                chromeOptions.addArguments("--no-sandbox");
                chromeOptions.addArguments("--disable-dev-shm-usage");
                DRIVER.set(new ChromeDriver(chromeOptions));
                break;

            case "firefox":
                WebDriverManager.firefoxdriver().setup();
                FirefoxOptions firefoxOptions = new FirefoxOptions();
                if (headless) {
                    firefoxOptions.addArguments("--headless");
                }
                DRIVER.set(new FirefoxDriver(firefoxOptions));
                break;

            case "edge":
                WebDriverManager.edgedriver().setup();
                DRIVER.set(new EdgeDriver());
                break;

            case "safari":
                DRIVER.set(new SafariDriver());
                break;

            default:
                LOGGER.error("Unsupported browser: {}", browser);
                throw new RuntimeException("Unsupported browser: " + browser);
        }

        LOGGER.info("{} browser set up successfully", browser);
        DRIVER.get().manage().window().maximize();
    }

    /**
     * Quits and removes the current thread's WebDriver instance.
     */
    public static void quitDriver() {
        if (DRIVER.get() != null) {
            LOGGER.info("Quitting WebDriver");
            DRIVER.get().quit();
            DRIVER.remove();
        }
    }
}
