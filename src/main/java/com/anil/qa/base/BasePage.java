package com.anil.qa.core;

import java.time.Duration;

import lombok.extern.slf4j.Slf4j;
import io.qameta.allure.Step;
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

import com.anil.qa.config.ConfigManager;
import com.anil.qa.utils.ReportManager;

/**
 * BasePage is the generic parent class for all page objects.
 * Provides common Selenium actions and Allure step logging.
 * @param <T> the type of the page object
 */
@Slf4j
public class BasePage<T extends BasePage<T>> {
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
    
    /**
     * Waits for the given element to be visible.
     * @param element the WebElement to wait for
     * @return the visible WebElement
     */
    @Step("Wait for element to be visible")
    public WebElement waitForElementToBeVisible(WebElement element) {
        try {
            log.debug("Waiting for element to be visible: {}", element);
            return wait.until(ExpectedConditions.visibilityOf(element));
        } catch (Exception e) {
            log.error("Element not visible: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Waits for the given element to be clickable.
     * @param element the WebElement to wait for
     * @return the clickable WebElement
     */
    @Step("Wait for element to be clickable")
    public WebElement waitForElementToBeClickable(WebElement element) {
        try {
            log.debug("Waiting for element to be clickable: {}", element);
            return wait.until(ExpectedConditions.elementToBeClickable(element));
        } catch (Exception e) {
            log.error("Element not clickable: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Clicks on the given element.
     * @param element the WebElement to click
     */
    @Step("Click on element")
    public void click(WebElement element) {
        try {
            waitForElementToBeClickable(element);
            log.debug("Clicking on element: {}", element);
            element.click();
        } catch (StaleElementReferenceException e) {
            log.warn("Stale element reference, retrying click operation", e);
            WebElement refreshedElement = wait.until(ExpectedConditions.refreshed(
                    ExpectedConditions.elementToBeClickable(element)));
            refreshedElement.click();
        } catch (Exception e) {
            log.error("Failed to click element: {}", element, e);
            throw e;
        }
    }
    
    protected void jsClick(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            log.debug("JS clicking on element: {}", element);
            js.executeScript("arguments[0].click();", element);
        } catch (Exception e) {
            log.error("Failed to JS click element: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Types text into the given element.
     * @param element the WebElement to type into
     * @param text the text to type
     */
    @Step("Type '{text}' in element")
    public void sendKeys(WebElement element, String text) {
        try {
            waitForElementToBeVisible(element);
            element.clear();
            log.debug("Typing text '{}' in element: {}", text, element);
            element.sendKeys(text);
        } catch (Exception e) {
            log.error("Failed to type text in element: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Selects an option by visible text from a dropdown.
     * @param element the dropdown WebElement
     * @param text the visible text to select
     */
    @Step("Select '{text}' from dropdown")
    public void selectByVisibleText(WebElement element, String text) {
        try {
            waitForElementToBeVisible(element);
            log.debug("Selecting option '{}' from dropdown: {}", text, element);
            new Select(element).selectByVisibleText(text);
        } catch (Exception e) {
            log.error("Failed to select option from dropdown: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Gets the text from the given element.
     * @param element the WebElement
     * @return the text of the element
     */
    @Step("Get text from element")
    public String getText(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            String text = element.getText();
            log.debug("Retrieved text '{}' from element: {}", text, element);
            return text;
        } catch (Exception e) {
            log.error("Failed to get text from element: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Checks if the element is displayed.
     * @param element the WebElement
     * @return true if displayed, false otherwise
     */
    public boolean isElementDisplayed(WebElement element) {
        try {
            return element.isDisplayed();
        } catch (NoSuchElementException | StaleElementReferenceException e) {
            return false;
        }
    }
    
    /**
     * Scrolls to the given element.
     * @param element the WebElement to scroll to
     */
    public void scrollToElement(WebElement element) {
        js.executeScript("arguments[0].scrollIntoView(true);", element);
        try {
            Thread.sleep(500); // Small pause for scroll to complete
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    /**
     * Hovers over the given element.
     * @param element the WebElement to hover over
     */
    public void hoverOverElement(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            actions.moveToElement(element).perform();
        } catch (Exception e) {
            log.error("Failed to hover over element: {}", element, e);
            throw e;
        }
    }
    
    /**
     * Logs a step in the report.
     * @param stepDescription the step description
     */
    @Step("Log step")
    public void logStep(String stepDescription) {
        log.info(stepDescription);
        ReportManager.logInfo(stepDescription);
    }
}