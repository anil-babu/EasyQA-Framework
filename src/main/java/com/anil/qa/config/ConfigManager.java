package com.anil.qa.config;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * ConfigManager handles loading and accessing configuration properties.
 */
public class ConfigManager {
    private static final Logger logger = LogManager.getLogger(ConfigManager.class);
    private static final Properties properties = new Properties();
    private static final String CONFIG_FILE_PATH = 
            "src/main/resources/config.properties";

    private ConfigManager() {
        // Private constructor to prevent instantiation
    }

    /**
     * Loads configuration from the properties file.
     */
    public static void loadConfig() {
        try (FileInputStream fis = new FileInputStream(CONFIG_FILE_PATH)) {
            logger.info("Loading configuration file: {}", CONFIG_FILE_PATH);
            properties.load(fis);
        } catch (IOException e) {
            logger.error("Failed to load configuration file: {}", 
                    CONFIG_FILE_PATH, e);
            throw new RuntimeException("Failed to load configuration file", e);
        }
    }

    /**
     * Gets a property value.
     * @param key the property key
     * @return the property value
     */
    public static String getProperty(String key) {
        String value = properties.getProperty(key);
        if (value == null) {
            logger.warn("Property not found in configuration: {}", key);
        }
        return value;
    }

    /**
     * Gets a property value with a default.
     * @param key the property key
     * @param defaultValue the default value
     * @return the property value or default
     */
    public static String getProperty(String key, String defaultValue) {
        return properties.getProperty(key, defaultValue);
    }

    /**
     * Sets a property value.
     * @param key the property key
     * @param value the property value
     */
    public static void setProperty(String key, String value) {
        properties.setProperty(key, value);
    }
}
