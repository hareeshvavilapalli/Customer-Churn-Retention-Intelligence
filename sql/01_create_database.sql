-- ==============================================================================
-- Project: Customer Churn & Retention Intelligence System
-- Script: 01_create_database.sql
-- Description: Creates the customer_churn_db database with enterprise configuration
-- Target RDBMS: MySQL 8.0+
-- Author: Senior Data Analyst
-- ==============================================================================

-- Drop database if it exists (for clean re-runs)
DROP DATABASE IF EXISTS customer_churn_db;

-- Create database with UTF-8 Unicode encoding
CREATE DATABASE customer_churn_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Switch to the newly created database context
USE customer_churn_db;

-- Verify database creation
SELECT 
    SCHEMA_NAME AS database_name,
    DEFAULT_CHARACTER_SET_NAME AS character_set,
    DEFAULT_COLLATION_NAME AS collation_name
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'customer_churn_db';
