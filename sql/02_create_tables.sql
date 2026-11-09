-- ==============================================================================
-- Project: Customer Churn & Retention Intelligence System
-- Script: 02_create_tables.sql
-- Description: DDL script creating consolidated and normalized relational tables
-- Target RDBMS: MySQL 8.0+
-- Author: Senior Data Analyst
-- ==============================================================================

USE customer_churn_db;

-- ------------------------------------------------------------------------------
-- 1. CONSOLIDATED MASTER TABLE: customers
-- Contains all 25 cleaned attributes and engineered features
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    -- Customer Identity & Demographics
    customerID VARCHAR(10) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    SeniorCitizen TINYINT NOT NULL,
    Partner VARCHAR(3) NOT NULL,
    Dependents VARCHAR(3) NOT NULL,
    
    -- Account Lifecycle
    tenure SMALLINT NOT NULL,
    
    -- Subscribed Voice & Data Services
    PhoneService VARCHAR(3) NOT NULL,
    MultipleLines VARCHAR(16) NOT NULL,
    InternetService VARCHAR(11) NOT NULL,
    OnlineSecurity VARCHAR(19) NOT NULL,
    OnlineBackup VARCHAR(19) NOT NULL,
    DeviceProtection VARCHAR(19) NOT NULL,
    TechSupport VARCHAR(19) NOT NULL,
    StreamingTV VARCHAR(19) NOT NULL,
    StreamingMovies VARCHAR(19) NOT NULL,
    
    -- Contractual & Payment Metadata
    Contract VARCHAR(14) NOT NULL,
    PaperlessBilling VARCHAR(3) NOT NULL,
    PaymentMethod VARCHAR(25) NOT NULL,
    
    -- Financial Metrics
    MonthlyCharges DECIMAL(10,2) NOT NULL,
    TotalCharges DECIMAL(10,2) NOT NULL,
    
    -- Target Variable
    Churn VARCHAR(3) NOT NULL,
    
    -- Engineered Analytical Features
    SeniorCitizen_Label VARCHAR(3) NOT NULL,
    tenure_group VARCHAR(10) NOT NULL,
    payment_category VARCHAR(10) NOT NULL,
    service_count TINYINT NOT NULL,
    
    -- Primary Key Constraint
    CONSTRAINT pk_customers PRIMARY KEY (customerID),
    
    -- Domain Integrity Constraints
    CONSTRAINT chk_tenure CHECK (tenure >= 0),
    CONSTRAINT chk_monthly_charges CHECK (MonthlyCharges >= 0.00),
    CONSTRAINT chk_total_charges CHECK (TotalCharges >= 0.00),
    CONSTRAINT chk_churn_values CHECK (Churn IN ('Yes', 'No')),
    CONSTRAINT chk_senior_values CHECK (SeniorCitizen IN (0, 1)),
    CONSTRAINT chk_gender_values CHECK (gender IN ('Male', 'Female')),
    CONSTRAINT chk_contract_values CHECK (Contract IN ('Month-to-month', 'One year', 'Two year'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Analytical Indexes for Fast Filter, Group By and Aggregation Performance
CREATE INDEX idx_customers_churn ON customers(Churn);
CREATE INDEX idx_customers_contract ON customers(Contract);
CREATE INDEX idx_customers_internet ON customers(InternetService);
CREATE INDEX idx_customers_payment ON customers(PaymentMethod);
CREATE INDEX idx_customers_tenure_grp ON customers(tenure_group);
CREATE INDEX idx_customers_pay_cat ON customers(payment_category);
CREATE INDEX idx_customers_contract_churn ON customers(Contract, Churn);
CREATE INDEX idx_customers_monthly_charges ON customers(MonthlyCharges);


-- ------------------------------------------------------------------------------
-- 2. NORMALIZED RELATIONAL SCHEMA (STAR / SNOWFLAKE MODEL)
-- Supports normalized data warehousing and relational JOIN operations
-- ------------------------------------------------------------------------------

-- Drop child tables first to respect foreign key constraints
DROP TABLE IF EXISTS fact_billing_churn;
DROP TABLE IF EXISTS dim_contracts;
DROP TABLE IF EXISTS dim_services;
DROP TABLE IF EXISTS dim_demographics;

-- A. Dimension: Demographics
CREATE TABLE dim_demographics (
    customerID VARCHAR(10) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    SeniorCitizen TINYINT NOT NULL,
    SeniorCitizen_Label VARCHAR(3) NOT NULL,
    Partner VARCHAR(3) NOT NULL,
    Dependents VARCHAR(3) NOT NULL,
    CONSTRAINT pk_dim_demographics PRIMARY KEY (customerID),
    CONSTRAINT fk_demo_customer FOREIGN KEY (customerID) 
        REFERENCES customers(customerID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- B. Dimension: Services Portfolio
CREATE TABLE dim_services (
    customerID VARCHAR(10) NOT NULL,
    PhoneService VARCHAR(3) NOT NULL,
    MultipleLines VARCHAR(16) NOT NULL,
    InternetService VARCHAR(11) NOT NULL,
    OnlineSecurity VARCHAR(19) NOT NULL,
    OnlineBackup VARCHAR(19) NOT NULL,
    DeviceProtection VARCHAR(19) NOT NULL,
    TechSupport VARCHAR(19) NOT NULL,
    StreamingTV VARCHAR(19) NOT NULL,
    StreamingMovies VARCHAR(19) NOT NULL,
    service_count TINYINT NOT NULL,
    CONSTRAINT pk_dim_services PRIMARY KEY (customerID),
    CONSTRAINT fk_services_customer FOREIGN KEY (customerID) 
        REFERENCES customers(customerID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- C. Dimension: Contracts & Billing Setup
CREATE TABLE dim_contracts (
    customerID VARCHAR(10) NOT NULL,
    Contract VARCHAR(14) NOT NULL,
    PaperlessBilling VARCHAR(3) NOT NULL,
    PaymentMethod VARCHAR(25) NOT NULL,
    payment_category VARCHAR(10) NOT NULL,
    tenure SMALLINT NOT NULL,
    tenure_group VARCHAR(10) NOT NULL,
    CONSTRAINT pk_dim_contracts PRIMARY KEY (customerID),
    CONSTRAINT fk_contracts_customer FOREIGN KEY (customerID) 
        REFERENCES customers(customerID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- D. Fact Table: Monthly & Cumulative Billing and Churn
CREATE TABLE fact_billing_churn (
    customerID VARCHAR(10) NOT NULL,
    MonthlyCharges DECIMAL(10,2) NOT NULL,
    TotalCharges DECIMAL(10,2) NOT NULL,
    Churn VARCHAR(3) NOT NULL,
    CONSTRAINT pk_fact_billing PRIMARY KEY (customerID),
    CONSTRAINT fk_billing_customer FOREIGN KEY (customerID) 
        REFERENCES customers(customerID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Populate Normalized Tables from the Master `customers` Table
-- (To be executed after data is loaded into `customers`)
-- INSERT INTO dim_demographics SELECT customerID, gender, SeniorCitizen, SeniorCitizen_Label, Partner, Dependents FROM customers;
-- INSERT INTO dim_services SELECT customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, service_count FROM customers;
-- INSERT INTO dim_contracts SELECT customerID, Contract, PaperlessBilling, PaymentMethod, payment_category, tenure, tenure_group FROM customers;
-- INSERT INTO fact_billing_churn SELECT customerID, MonthlyCharges, TotalCharges, Churn FROM customers;
