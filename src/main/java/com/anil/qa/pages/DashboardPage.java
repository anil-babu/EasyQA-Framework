
package com.anil.qa.pages;
import com.anil.qa.base.BasePage;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

/**
 * Page object for the Dashboard page.
 * Provides methods to verify dashboard state.
 */

public class DashboardPage extends BasePage {
    /**
     * Constructs a DashboardPage object.
     * @param driver the WebDriver instance
     */
    public DashboardPage(final WebDriver driver) {
        super(driver);
    }


    /**
     * Dashboard title element.
     */
    @FindBy(xpath = "//h1[contains(text(), 'Dashboard')]")
    private WebElement dashboardTitle;

    /**
     * Checks if the dashboard is displayed.
     * @return true if displayed, false otherwise
     */
    public boolean isDashboardDisplayed() {
        return dashboardTitle.isDisplayed();
    }
}
