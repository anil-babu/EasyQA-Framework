package com.anil.qa.utils;

import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

public class ApiUtils {
    private static final Logger logger = LogManager.getLogger(ApiUtils.class);
    
    private ApiUtils() {
        // Private constructor to prevent instantiation
    }
    
    public static Response get(String endpoint) {
        return get(endpoint, null, null);
    }
    
    public static Response get(String endpoint, Map<String, String> headers) {
        return get(endpoint, headers, null);
    }
    
    public static Response get(String endpoint, Map<String, String> headers, Map<String, String> queryParams) {
        logger.info("Making GET request to: {}", endpoint);
        RequestSpecification request = RestAssured.given().log().all();
        
        if (headers != null) {
            request.headers(headers);
        }
        
        if (queryParams != null) {
            request.queryParams(queryParams);
        }
        
        Response response = request.get(endpoint);
        logger.info("Response received with status code: {}", response.getStatusCode());
        
        return response;
    }
    
    public static Response post(String endpoint, Object body) {
        return post(endpoint, body, null, ContentType.JSON);
    }
    
    public static Response post(String endpoint, Object body, Map<String, String> headers) {
        return post(endpoint, body, headers, ContentType.JSON);
    }
    
    public static Response post(String endpoint, Object body, Map<String, String> headers, ContentType contentType) {
        logger.info("Making POST request to: {}", endpoint);
        RequestSpecification request = RestAssured.given().log().all();
        
        if (headers != null) {
            request.headers(headers);
        }
        
        if (body != null) {
            request.contentType(contentType).body(body);
        }
        
        Response response = request.post(endpoint);
        logger.info("Response received with status code: {}", response.getStatusCode());
        
        return response;
    }
    
    public static Response put(String endpoint, Object body) {
        return put(endpoint, body, null);
    }
    
    public static Response put(String endpoint, Object body, Map<String, String> headers) {
        logger.info("Making PUT request to: {}", endpoint);
        RequestSpecification request = RestAssured.given().log().all();
        
        if (headers != null) {
            request.headers(headers);
        }
        
        if (body != null) {
            request.contentType(ContentType.JSON).body(body);
        }
        
        Response response = request.put(endpoint);
        logger.info("Response received with status code: {}", response.getStatusCode());
        
        return response;
    }
    
    public static Response delete(String endpoint) {
        return delete(endpoint, null);
    }
    
    public static Response delete(String endpoint, Map<String, String> headers) {
        logger.info("Making DELETE request to: {}", endpoint);
        RequestSpecification request = RestAssured.given().log().all();
        
        if (headers != null) {
            request.headers(headers);
        }
        
        Response response = request.delete(endpoint);
        logger.info("Response received with status code: {}", response.getStatusCode());
        
        return response;
    }
    
    public static String getJsonPath(Response response, String path) {
        return response.jsonPath().getString(path);
    }
}