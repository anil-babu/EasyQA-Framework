package com.anil.qa.tests;

import com.anil.qa.base.BaseTest;
import io.restassured.response.Response;
import org.testng.Assert;
import org.testng.annotations.Test;
import com.anil.qa.utils.ApiUtils;

public class ApiTests extends BaseTest {

    @Test
    public void verifyGetUsersAPI() {
        Response response = ApiUtils.get("https://jsonplaceholder.typicode.com/users");
        Assert.assertEquals(response.getStatusCode(), 200, "Status code should be 200");
    }
}
