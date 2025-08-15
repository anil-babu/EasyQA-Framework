package com.anil.qa.utils;

import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

/**
 * ApiUtils provides static methods for REST API calls using RestAssured.
 * Supports GET, POST, PUT, DELETE, and JSON path extraction.
 */
public class ApiUtils {
    private static final Logger logger = LogManager.getLogger(ApiUtils.class);
    
    private ApiUtils() {
        // Private constructor to prevent instantiation
    }
    
    /**
     * Makes a GET request to the given endpoint.
     * @param endpoint the API endpoint
     * @return the Response
     */
    public static Response get(String endpoint) {
        return get(endpoint, null, null);
    }
    
    /**
     * Makes a GET request to the given endpoint with headers.
     * @param endpoint the API endpoint
     * @param headers the request headers
     * @return the Response
     */
    public static Response get(String endpoint, Map<String, String> headers) {
        return get(endpoint, headers, null);
    }
    
    /**
     * Makes a GET request to the given endpoint with headers and query parameters.
     * @param endpoint the API endpoint
     * @param headers the request headers
     * @param queryParams the request query parameters
     * @return the Response
     */
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
    
    /**
     * Makes a POST request to the given endpoint with a body.
     * @param endpoint the API endpoint
     * @param body the request body
     * @return the Response
     */
    public static Response post(String endpoint, Object body) {
        return post(endpoint, body, null, ContentType.JSON);
    }
    
    /**
     * Makes a POST request to the given endpoint with a body and headers.
     * @param endpoint the API endpoint
     * @param body the request body
     * @param headers the request headers
     * @return the Response
     */
    public static Response post(String endpoint, Object body, Map<String, String> headers) {
        return post(endpoint, body, headers, ContentType.JSON);
    }
    
    /**
     * Makes a POST request to the given endpoint with a body, headers, and content type.
     * @param endpoint the API endpoint
     * @param body the request body
     * @param headers the request headers
     * @param contentType the content type of the request body
     * @return the Response
     */
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
    
    /**
     * Makes a PUT request to the given endpoint with a body.
     * @param endpoint the API endpoint
     * @param body the request body
     * @return the Response
     */
    public static Response put(String endpoint, Object body) {
        return put(endpoint, body, null);
    }
    
    /**
     * Makes a PUT request to the given endpoint with a body and headers.
     * @param endpoint the API endpoint
     * @param body the request body
     * @param headers the request headers
     * @return the Response
     */
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
    
    /**
     * Makes a DELETE request to the given endpoint.
     * @param endpoint the API endpoint
     * @return the Response
     */
    public static Response delete(String endpoint) {
        return delete(endpoint, null);
    }
    
    /**
     * Makes a DELETE request to the given endpoint with headers.
     * @param endpoint the API endpoint
     * @param headers the request headers
     * @return the Response
     */
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
    
    /**
     * Extracts a value from a JSON response using a JSON path.
     * @param response the Response
     * @param path the JSON path
     * @return the value as String
     */
    public static String getJsonPath(Response response, String path) {
        return response.jsonPath().getString(path);
    }
}