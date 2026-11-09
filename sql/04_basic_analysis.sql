-- ==============================================================================
-- Project: Customer Churn & Retention Intelligence System
-- Script: 04_basic_analysis.sql
-- Description: Core exploratory, demographic, and service adoption SQL queries
-- Target RDBMS: MySQL 8.0+
-- Author: Senior Data Analyst
-- ==============================================================================

USE customer_churn_db;

-- ------------------------------------------------------------------------------
-- QUERY 1: Overall Customer Volume and Churn Distribution
-- ------------------------------------------------------------------------------
-- Business Question:
-- What is the total customer volume, count of retained vs. churned subscribers,
-- and the baseline portfolio churn rate across the company?
--
-- Explanation of Logic:
-- Uses COUNT(*) to aggregate total records and conditional aggregation (SUM with CASE WHEN)
-- to segment retained ('No') and churned ('Yes') subscribers, computing baseline percentages.

SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS retention_rate_pct
FROM customers;

-- Expected Business Insight:
-- Confirms a total of 7,043 customers, with 5,174 retained (73.46%) and 1,869 churned (26.54%).
-- Establishes the 26.54% churn rate as the benchmark benchmark for all subsequent segment comparisons.


-- ------------------------------------------------------------------------------
-- QUERY 2: Demographic Distribution (Gender, Partner, Dependents)
-- ------------------------------------------------------------------------------
-- Business Question:
-- How are subscribers distributed across demographic segments (gender, marital status,
-- and dependents), and which demographic cohort experiences the highest attrition?
--
-- Explanation of Logic:
-- Groups customers by gender, Partner, and Dependents, calculating cohort headcount,
-- share of the total subscriber base, and segment-specific churn rates.

SELECT 
    gender,
    Partner,
    Dependents,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS pct_of_total_base,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS segment_churn_rate_pct
FROM customers
GROUP BY gender, Partner, Dependents
ORDER BY customer_count DESC;

-- Expected Business Insight:
-- Subscribers living alone without a partner or dependents exhibit significantly higher churn
-- (Females alone: 35.47%, Males alone: 32.98%). In contrast, family households with both
-- a partner and dependents show strong loyalty, churning at only 13.51% (Males) and 14.95% (Females).


-- ------------------------------------------------------------------------------
-- QUERY 3: Senior Citizen Churn Comparison
-- ------------------------------------------------------------------------------
-- Business Question:
-- How does customer retention differ between Senior Citizens and Non-Senior Citizens?
--
-- Explanation of Logic:
-- Aggregates customer count and churn counts by the `SeniorCitizen` flag and user-friendly
-- `SeniorCitizen_Label` to quantify age-bracket vulnerability.

SELECT 
    SeniorCitizen,
    SeniorCitizen_Label,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY SeniorCitizen, SeniorCitizen_Label
ORDER BY SeniorCitizen;

-- Expected Business Insight:
-- Senior citizens (1,142 customers) experience a severe 41.68% churn rate, compared to 23.61%
-- among non-senior subscribers (5,901 customers). This indicates that senior subscribers may be
-- disproportionately affected by fixed-income pricing, billing complexity, or inadequate tech support.


-- ------------------------------------------------------------------------------
-- QUERY 4: Top 10 Highest-Paying Active Subscribers
-- ------------------------------------------------------------------------------
-- Business Question:
-- Who are the top 10 highest-value active subscribers currently retained in the portfolio,
-- and what are their contract and payment profiles?
--
-- Explanation of Logic:
-- Filters for active accounts (`Churn = 'No'`), orders descending by `MonthlyCharges`,
-- and limits the result set to the top 10 individual accounts.

SELECT 
    customerID,
    gender,
    tenure,
    Contract,
    InternetService,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges
FROM customers
WHERE Churn = 'No'
ORDER BY MonthlyCharges DESC
LIMIT 10;

-- Expected Business Insight:
-- The highest-paying retained customers generate up to $118.75/month (led by customer 7569-NMZYQ).
-- Nearly all top accounts utilize Fiber Optic internet, have completed 68-72 months of tenure,
-- are locked into Two-Year contracts, and have accumulated over $8,000 in lifetime revenue.


-- ------------------------------------------------------------------------------
-- QUERY 5: Core Phone Service & Multiple Lines Adoption
-- ------------------------------------------------------------------------------
-- Business Question:
-- What proportion of subscribers utilize voice landlines, and does having multiple lines
-- correlate with greater customer retention?
--
-- Explanation of Logic:
-- Groups subscribers by `PhoneService` and `MultipleLines`, calculating total subscriber volume,
-- churn counts, and segment churn percentages.

SELECT 
    PhoneService,
    MultipleLines,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churn_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY PhoneService, MultipleLines
ORDER BY customer_count DESC;

-- Expected Business Insight:
-- Phone service is held by 90.3% of customers (6,361). Customers with multiple lines churn at 28.61%,
-- compared to 25.04% for single-line voice and 24.93% for customers without phone service.
-- Voice tiering alone does not provide a strong protective retention barrier.


-- ------------------------------------------------------------------------------
-- QUERY 6: Contract Commitment Term Distribution
-- ------------------------------------------------------------------------------
-- Business Question:
-- What is the portfolio distribution across contract terms, and how do monthly charges
-- and customer tenure vary across commitment lengths?
--
-- Explanation of Logic:
-- Aggregates customer count, percentage of customer base, average monthly billing,
-- and average tenure across Month-to-month, One year, and Two year contracts.

SELECT 
    Contract,
    COUNT(*) AS subscriber_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS pct_of_base,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(tenure), 1) AS avg_tenure_months
FROM customers
GROUP BY Contract
ORDER BY subscriber_count DESC;

-- Expected Business Insight:
-- Month-to-month agreements dominate the portfolio (55.02%, 3,875 subscribers) with an average
-- tenure of only 18.0 months. Multi-year contract holders (24.07% Two-year, 20.91% One-year)
-- demonstrate much longer customer lifespans (56.7 months and 42.0 months respectively).
