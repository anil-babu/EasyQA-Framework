package com.anil.qa.utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

/**
 * IExcelUtils defines contract for Excel data utilities.
 */
public interface IExcelUtils {
    /**
     * Reads test data from an Excel file and returns it as a 2D Object array.
     * @param filePath the path to the Excel file
     * @param sheetName the sheet name
     * @return test data as Object[][]
     */
    Object[][] getTestData(String filePath, String sheetName);
}

/**
 * ExcelUtils provides static and instance methods for reading test data from Excel files.
 * Supports data-driven testing for TestNG.
 */
public class ExcelUtils implements IExcelUtils {
    private static final Logger logger = LogManager.getLogger(ExcelUtils.class);
    
    private ExcelUtils() {
        // Private constructor to prevent instantiation
    }
    
    @Override
    public Object[][] getTestData(String filePath, String sheetName) {
        try (FileInputStream fis = new FileInputStream(filePath);
             Workbook workbook = new XSSFWorkbook(fis)) {
            
            Sheet sheet = workbook.getSheet(sheetName);
            int rowCount = sheet.getLastRowNum();
            int colCount = sheet.getRow(0).getLastCellNum();
            
            Object[][] data = new Object[rowCount][1];
            
            for (int i = 0; i < rowCount; i++) {
                Map<String, String> map = new HashMap<>();
                
                for (int j = 0; j < colCount; j++) {
                    String key = sheet.getRow(0).getCell(j).getStringCellValue();
                    String value = getCellValueAsString(sheet.getRow(i + 1).getCell(j));
                    map.put(key, value);
                }
                
                data[i][0] = map;
            }
            
            logger.info("Test data loaded from Excel: {} rows, {} columns", rowCount, colCount);
            return data;
            
        } catch (IOException e) {
            logger.error("Failed to load test data from Excel file: {}", filePath, e);
            throw new RuntimeException("Failed to load test data from Excel file", e);
        }
    }
    
    /**
     * Reads test data from an Excel file and returns it as a List of Maps.
     * @param filePath the path to the Excel file
     * @param sheetName the sheet name
     * @return test data as List<Map<String, String>>
     */
    public static List<Map<String, String>> getTestDataAsList(String filePath, String sheetName) {
        List<Map<String, String>> testDataList = new ArrayList<>();
        
        try (FileInputStream fis = new FileInputStream(filePath);
             Workbook workbook = new XSSFWorkbook(fis)) {
            
            Sheet sheet = workbook.getSheet(sheetName);
            int rowCount = sheet.getLastRowNum();
            int colCount = sheet.getRow(0).getLastCellNum();
            
            // Get header row for column names
            Row headerRow = sheet.getRow(0);
            List<String> headers = new ArrayList<>();
            for (int i = 0; i < colCount; i++) {
                headers.add(headerRow.getCell(i).getStringCellValue());
            }
            
            // Iterate through data rows
            for (int i = 1; i <= rowCount; i++) {
                Row dataRow = sheet.getRow(i);
                Map<String, String> dataMap = new HashMap<>();
                
                for (int j = 0; j < colCount; j++) {
                    String header = headers.get(j);
                    String value = getCellValueAsString(dataRow.getCell(j));
                    dataMap.put(header, value);
                }
                
                testDataList.add(dataMap);
            }
            
            logger.info("Test data loaded as list from Excel: {} rows", testDataList.size());
            return testDataList;
            
        } catch (IOException e) {
            logger.error("Failed to load test data as list from Excel file: {}", filePath, e);
            throw new RuntimeException("Failed to load test data as list from Excel file", e);
        }
    }
    
    /**
     * Provides data for TestNG DataProvider.
     * @param filePath the path to the Excel file
     * @param sheetName the sheet name
     * @return test data as Object[][]
     */
    public static Object[][] provideData(String filePath, String sheetName) {
        return new ExcelUtils().getTestData(filePath, sheetName);
    }
    
    private static String getCellValueAsString(Cell cell) {
        if (cell == null) {
            return "";
        }
        
        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue();
            case NUMERIC:
                return String.valueOf(cell.getNumericCellValue());
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            case FORMULA:
                return cell.getCellFormula();
            default:
                return "";
        }
    }
}