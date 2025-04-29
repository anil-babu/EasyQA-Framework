package com.anil.qa.pages;
import com.anil.qa.base.BasePage;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

public class DashboardPage extends BasePage {
	public DashboardPage(WebDriver driver) {
	    super(driver);
	}

    @FindBy(xpath = "//h1[contains(text(), 'Dashboard')]")
    private WebElement dashboardTitle;

    public boolean isDashboardDisplayed() {
        return dashboardTitle.isDisplayed();
    }
}