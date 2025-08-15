package com.anil.qa.utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * ConfigManager handles loading and accessing configuration properties.
 */
public final class ConfigManager {
    /** Logger instance. */
    private static final Logger LOGGER = LogManager.getLogger(ConfigManager.class);
    /** Properties instance. */
    private static final Properties PROPERTIES = new Properties();
    /** Config file path. */
    private static final String CONFIG_FILE_PATH = "src/main/resources/config.properties";

    private ConfigManager() {
        // Private constructor to prevent instantiation
    }

    /**
     * Loads the configuration file.
     */
    public static void loadConfig() {
        try (FileInputStream fis = new FileInputStream(CONFIG_FILE_PATH)) {
            LOGGER.info("Loading configuration file: {}", CONFIG_FILE_PATH);
            PROPERTIES.load(fis);
        } catch (final IOException e) {
            LOGGER.error("Failed to load configuration file: {}", CONFIG_FILE_PATH, e);
            throw new RuntimeException("Failed to load configuration file", e);
        }
    }

    /**
     * Gets a property value by key.
     * @param key the property key
     * @return the property value, or null if not found
     */
    public static String getProperty(final String key) {
        String value = PROPERTIES.getProperty(key);
        if (value == null) {
            LOGGER.warn("Property not found in configuration: {}", key);
        }
        return value;
    }

    /**
     * Gets a property value by key, with a default value.
     * @param key the property key
     * @param defaultValue the default value
     * @return the property value, or defaultValue if not found
     */
    public static String getProperty(final String key, final String defaultValue) {
        return PROPERTIES.getProperty(key, defaultValue);
    }

    /**
     * Sets a property value by key.
     * @param key the property key
     * @param value the value to set
     */
    public static void setProperty(final String key, final String value) {
        PROPERTIES.setProperty(key, value);
    }
}
