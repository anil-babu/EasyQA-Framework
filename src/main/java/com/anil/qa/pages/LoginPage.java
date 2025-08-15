package com.anil.qa.pages;

import com.anil.qa.core.BasePage;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import io.qameta.allure.Step;

/**
 * Page object for the Login page.
 * Provides login functionality for tests.
 */
public class LoginPage extends BasePage {
	
	public LoginPage(WebDriver driver) {
        super(driver);
    }
	
	
	 @FindBy(id = "username")
	    private WebElement usernameInput;

	    @FindBy(id = "password")
	    private WebElement passwordInput;

	    @FindBy(id = "loginButton")
	    private WebElement loginButton;

	    /**
	     * Logs in with the given username and password.
	     * @param username the username
	     * @param password the password
	     */
	    @Step("Login as user: {username}")
	    public void login(String username, String password) {
	        usernameInput.sendKeys(username);
	        passwordInput.sendKeys(password);
	        loginButton.click();
	    }

}
