-- ==============================================================================
-- Project: Customer Churn & Retention Intelligence System
-- Script: 03_load_data.sql
-- Description: Bulk data loading script for MySQL using LOAD DATA INFILE
-- Target RDBMS: MySQL 8.0+
-- Author: Senior Data Analyst
-- ==============================================================================

USE customer_churn_db;

-- ------------------------------------------------------------------------------
-- Configuration Note for MySQL Server Administrators:
-- If using MySQL Workbench or CLI with local files:
-- 1. Ensure `local_infile` is enabled on the server:
--    SET GLOBAL local_infile = 1;
-- 2. Connect client with `--local-infile=1`.
-- 3. Replace the placeholder filepath below with your system's absolute path:
--    e.g., 'C:/Users/V.Leela prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/dataset/cleaned_telco_customer_churn.csv'
--    or place file inside the MySQL `secure_file_priv` directory.
-- Alternatively, use `python/load_to_mysql.py` for automated programmatic loading.
-- ------------------------------------------------------------------------------

-- Step 1: Temporarily disable foreign key checks to safely truncate existing tables
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE dim_demographics;
TRUNCATE TABLE dim_services;
TRUNCATE TABLE dim_contracts;
TRUNCATE TABLE fact_billing_churn;
TRUNCATE TABLE customers;

SET FOREIGN_KEY_CHECKS = 1;

-- Step 2: Bulk load cleaned CSV into `customers`
LOAD DATA LOCAL INFILE 'C:/Users/V.Leela prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/dataset/cleaned_telco_customer_churn.csv'
INTO TABLE customers
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges,
    Churn,
    SeniorCitizen_Label,
    tenure_group,
    payment_category,
    service_count
);

-- Step 3: Populate Normalized Dimension & Fact Tables
-- (Executed after master table loading)
INSERT INTO dim_demographics (customerID, gender, SeniorCitizen, SeniorCitizen_Label, Partner, Dependents)
SELECT customerID, gender, SeniorCitizen, SeniorCitizen_Label, Partner, Dependents
FROM customers;

INSERT INTO dim_services (customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, service_count)
SELECT customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, service_count
FROM customers;

INSERT INTO dim_contracts (customerID, Contract, PaperlessBilling, PaymentMethod, payment_category, tenure, tenure_group)
SELECT customerID, Contract, PaperlessBilling, PaymentMethod, payment_category, tenure, tenure_group
FROM customers;

INSERT INTO fact_billing_churn (customerID, MonthlyCharges, TotalCharges, Churn)
SELECT customerID, MonthlyCharges, TotalCharges, Churn
FROM customers;

-- Step 4: Verify record count in all tables
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'dim_demographics', COUNT(*) FROM dim_demographics
UNION ALL
SELECT 'dim_services', COUNT(*) FROM dim_services
UNION ALL
SELECT 'dim_contracts', COUNT(*) FROM dim_contracts
UNION ALL
SELECT 'fact_billing_churn', COUNT(*) FROM fact_billing_churn;
