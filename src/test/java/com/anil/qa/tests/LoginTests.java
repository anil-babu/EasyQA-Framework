package com.anil.qa.tests;

import com.anil.qa.base.BaseTest;
import com.anil.qa.base.DriverManager;

import org.testng.Assert;
import org.testng.annotations.Test;
import com.anil.qa.pages.LoginPage;
import com.anil.qa.pages.DashboardPage;

public class LoginTests extends BaseTest {

    @Test
    public void verifySuccessfulLogin() {
        LoginPage loginPage = new LoginPage(DriverManager.getDriver());
        loginPage.login("admin", "password123");

        DashboardPage dashboardPage = new DashboardPage(DriverManager.getDriver());
        Assert.assertTrue(dashboardPage.isDashboardDisplayed(), "Dashboard should be displayed after login");
    }
}