package com.anil.qa.base;
import java.time.Duration;
import io.qameta.allure.Step;
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
public class BasePage<T extends BasePage<T>> {
    /** WebDriver instance. */
    private final WebDriver driver;
    /** WebDriverWait instance. */
    private final WebDriverWait wait;
    /** Actions instance. */
    private final Actions actions;
    /** JavascriptExecutor instance. */
    private final JavascriptExecutor js;

    /**
     * Constructs a BasePage object.
     * @param webDriver the WebDriver instance
     */
    protected BasePage(final WebDriver webDriver) {
        this.driver = webDriver;
        int waitTime = Integer.parseInt(
            ConfigManager.getProperty("wait.time.seconds", "30")
        );
        this.wait = new WebDriverWait(webDriver, Duration.ofSeconds(waitTime));
        this.actions = new Actions(webDriver);
        this.js = (JavascriptExecutor) webDriver;
        PageFactory.initElements(webDriver, this);
    }

    /**
     * Waits for the given element to be visible.
     * @param element the WebElement to wait for
     * @return the visible WebElement
     */
    @Step("Wait for element to be visible")
    public WebElement waitForElementToBeVisible(final WebElement element) {
        try {
            return wait.until(ExpectedConditions.visibilityOf(element));
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Waits for the given element to be clickable.
     * @param element the WebElement to wait for
     * @return the clickable WebElement
     */
    @Step("Wait for element to be clickable")
    public WebElement waitForElementToBeClickable(final WebElement element) {
        try {
            return wait.until(ExpectedConditions.elementToBeClickable(element));
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Clicks on the given element.
     * @param element the WebElement to click
     */
    @Step("Click on element")
    public void click(final WebElement element) {
        try {
            waitForElementToBeClickable(element);
            element.click();
        } catch (final StaleElementReferenceException e) {
            WebElement refreshedElement = wait.until(
                ExpectedConditions.refreshed(
                    ExpectedConditions.elementToBeClickable(element)
                )
            );
            refreshedElement.click();
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Clicks on the given element using JavaScript.
     * @param element the WebElement to click
     */
    protected void jsClick(WebElement element) {
        try {
            waitForElementToBeVisible(element);
            js.executeScript(
                "arguments[0].click();",
                element
            );
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Types text into the given element.
     * @param element the WebElement to type into
     * @param text the text to type
     */
    @Step("Type '{text}' in element")
    public void sendKeys(final WebElement element, final String text) {
        try {
            waitForElementToBeVisible(element);
            element.clear();
            element.sendKeys(text);
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
    * Selects an option by visible text from a dropdown.
    * @param element the dropdown WebElement
    * @param text the visible text to select
     */
    @Step("Select '{text}' from dropdown")
    public void selectByVisibleText(
        final WebElement element,
        final String text
    ) {
        try {
            waitForElementToBeVisible(element);
            Select select = new Select(element);
            select
                .selectByVisibleText(
                    text
                );
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Gets the text from the given element.
     * @param element the WebElement
     * @return the text of the element
     */
    @Step("Get text from element")
    public String getText(final WebElement element) {
        try {
            waitForElementToBeVisible(element);
            String textValue = element.getText();
            return textValue;
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Checks if the element is displayed.
     * @param element the WebElement
     * @return true if displayed, false otherwise
     */
    public boolean isElementDisplayed(final WebElement element) {
        try {
            return element.isDisplayed();
        } catch (
            final NoSuchElementException
            | StaleElementReferenceException e
        ) {
            return false;
        }
    }

    // Removed duplicate/partial scrollToElement and SCROLL_PAUSE_MS
    /**
    * Scrolls to the given element.
    * Subclasses overriding this method should ensure that the scroll action is
    * safe and does not interfere with other actions.
    * This method is final to prevent unsafe overrides.
    * @param element the WebElement to scroll to
     */
    private static final int SCROLL_PAUSE_MS = 500;
    public final void scrollToElement(final WebElement element) {
        js.executeScript(
            "arguments[0].scrollIntoView(true);",
            element
        );
        try {
            // Small pause for scroll to complete
            Thread.sleep(SCROLL_PAUSE_MS);
        } catch (final InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    /**
     * Hovers over the given element.
     * @param element the WebElement to hover over
     */
    public void hoverOverElement(final WebElement element) {
        try {
            waitForElementToBeVisible(element);
            actions.moveToElement(element).perform();
        } catch (final Exception e) {
            throw e;
        }
    }

    /**
     * Logs a step in the report.
     * @param stepDescription the step description
     */
    @Step("Log step")
    public void logStep(final String stepDescription) {
    // Logging removed
        ReportManager.logInfo(stepDescription);
    }
}
