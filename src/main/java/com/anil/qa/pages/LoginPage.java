package com.anil.qa.pages;

import com.anil.qa.base.BasePage;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

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

	    public void login(String username, String password) {
	        usernameInput.sendKeys(username);
	        passwordInput.sendKeys(password);
	        loginButton.click();
	    }

}
