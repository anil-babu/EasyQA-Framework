package com.anil.qa.utils;

/**
 * IExcelUtils defines contract for Excel data utilities.
 */
public interface IExcelUtils {
    /**
     * Reads test data from an Excel file.
     * @param filePath the path to the Excel file
     * @param sheetName the sheet name
     * @return test data as Object[][]
     */
    Object[][] getTestData(String filePath, String sheetName);
}
