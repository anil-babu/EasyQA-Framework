package com.anil.qa.pages;

import com.anil.qa.base.BasePage;

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

    /**
     * Username input field.
     */
    @FindBy(id = "username")
    private WebElement usernameInput;

    /**
     * Password input field.
     */
    @FindBy(id = "password")
    private WebElement passwordInput;

    /**
     * Login button.
     */
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

