package com.anil.qa.base;

import java.time.Duration;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;

import com.anil.qa.utils.ConfigManager;
import com.anil.qa.utils.ReportManager;

public class BasePage {
    private static final Logger logger = LogManager.getLogger(BasePage.class);
    protected WebDriver driver;
    protected WebDriverWait wait;
    protected Actions actions;
    protected JavascriptExecutor js;
    
    
    protected BasePage(WebDriver driver) {
        this.driver = driver;
        int waitTime = Integer.parseInt(ConfigManager.getProperty("wait.time.seconds", "30"));
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(waitTime));
        this.actions = new Actions(driver);
        this.js = (JavascriptExecutor) driver;
        PageFactory.initElements(driver, this);
    }
    
    protected WebElement waitForElementToBeVisible(WebElement element) {
        try {
            logger.debug("Waiting for element to be visible: {}", element);
            return wait.until(ExpectedConditions.visibilityOf(element));
        } catch (Exception e) {
            logger.error("Element not visible: {}", element, e);
            throw e;
        }
    }
    
    protected WebElement waitForElementToBeClickable(WebElement element) {
        try {
            logger.debug("Waiting for element to be clickable: {}", element);
            return wait.until(ExpectedConditions.elementToBeClickable(element));
        } catch (Exception e) {
            logger.error("Element not clickable: {}", element, e);
            throw e;
        }
    }
    
    protected void click(WebElement element) {
        try {
            waitForElementToBeClickable(element);
            logger.debug("Clicking on element: {}", element);
            element.click();
        } catch (StaleElementReferenceException e) {
            logger.warn("Stale element reference, retrying click operation", e);
            WebElement refreshedElement = wait.until(ExpectedConditions.refreshed(
                    ExpectedConditions.elementToBeClickable(element)));
            refreshedElement.click();
        } catch (Exception e) {
            logger.error("Failed to click element: {}", element, e);
            throw e;
        }
    }
    
    protected void jsClick(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            logger.debug("JS clicking on element: {}", element);
            js.executeScript("arguments[0].click();", element);
        } catch (Exception e) {
            logger.error("Failed to JS click element: {}", element, e);
            throw e;
        }
    }
    
    protected void sendKeys(WebElement element, String text) {
        try {
            waitForElementToBeVisible(element);
            element.clear();
            logger.debug("Typing text '{}' in element: {}", text, element);
            element.sendKeys(text);
        } catch (Exception e) {
            logger.error("Failed to type text in element: {}", element, e);
            throw e;
        }
    }
    
    protected void selectByVisibleText(WebElement element, String text) {
        try {
            waitForElementToBeVisible(element);
            logger.debug("Selecting option '{}' from dropdown: {}", text, element);
            new Select(element).selectByVisibleText(text);
        } catch (Exception e) {
            logger.error("Failed to select option from dropdown: {}", element, e);
            throw e;
        }
    }
    
    protected String getText(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            String text = element.getText();
            logger.debug("Retrieved text '{}' from element: {}", text, element);
            return text;
        } catch (Exception e) {
            logger.error("Failed to get text from element: {}", element, e);
            throw e;
        }
    }
    
    protected boolean isElementDisplayed(WebElement element) {
        try {
            return element.isDisplayed();
        } catch (NoSuchElementException | StaleElementReferenceException e) {
            return false;
        }
    }
    
    protected void scrollToElement(WebElement element) {
        js.executeScript("arguments[0].scrollIntoView(true);", element);
        try {
            Thread.sleep(500); // Small pause for scroll to complete
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    protected void hoverOverElement(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            actions.moveToElement(element).perform();
        } catch (Exception e) {
            logger.error("Failed to hover over element: {}", element, e);
            throw e;
        }
    }
    
    protected void logStep(String stepDescription) {
        logger.info(stepDescription);
        ReportManager.logInfo(stepDescription);
    }
}