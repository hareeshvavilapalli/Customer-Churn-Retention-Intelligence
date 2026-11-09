-- ==============================================================================
-- Project: Customer Churn & Retention Intelligence System
-- Script: 07_advanced_analysis.sql
-- Description: Advanced analytical queries utilizing CTEs, Window Functions, and Multi-Table JOINs
-- Target RDBMS: MySQL 8.0+
-- Author: Senior Data Analyst
-- ==============================================================================

USE customer_churn_db;

-- ------------------------------------------------------------------------------
-- QUERY 20: CTE - Customer Lifetime Value (LTV) Tier Segmentation
-- ------------------------------------------------------------------------------
-- Business Question:
-- How can customers be segmented into Lifetime Value (LTV) tiers based on cumulative billing,
-- and how does churn rate differ across low, medium, high, and VIP value bands?
--
-- Explanation of Logic:
-- Uses a Common Table Expression (CTE) `Customer_LTV_Tiers` with a CASE expression to classify
-- customers into 4 financial tiers (<$500, $500-$2.5k, $2.5k-$5k, >$5k), then aggregates
-- subscriber counts, churn counts, churn rate, and cumulative revenue in the outer query.

WITH Customer_LTV_Tiers AS (
    SELECT 
        customerID,
        MonthlyCharges,
        TotalCharges,
        Churn,
        CASE 
            WHEN TotalCharges < 500 THEN '1. Low LTV (< $500)'
            WHEN TotalCharges BETWEEN 500 AND 2500 THEN '2. Medium LTV ($500-$2.5k)'
            WHEN TotalCharges BETWEEN 2500 AND 5000 THEN '3. High LTV ($2.5k-$5k)'
            ELSE '4. VIP LTV (> $5k)'
        END AS ltv_tier
    FROM customers
)
SELECT 
    ltv_tier,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(TotalCharges), 2) AS total_revenue
FROM Customer_LTV_Tiers
GROUP BY ltv_tier
ORDER BY ltv_tier;

-- Expected Business Insight:
-- Customers in the Low LTV tier (<$500) exhibit a 43.19% churn rate (999 churners out of 2,313 customers).
-- As cumulative spend and relationship duration grow, churn falls steadily to 26.68% (Medium),
-- 21.00% (High), and drops to just 15.48% for VIP accounts who have spent over $5,000.


-- ------------------------------------------------------------------------------
-- QUERY 21: CTE - Service Portfolio Depth (Service Count) vs. Churn Likelihood
-- ------------------------------------------------------------------------------
-- Business Question:
-- Does subscribing to a broader bundle of services increase customer retention,
-- and what is the optimal service bundle threshold to minimize churn?
--
-- Explanation of Logic:
-- Uses a CTE `Service_Depth` grouping by the engineered feature `service_count` (range 1-9),
-- computing customer counts, churned volume, and average monthly charges.

WITH Service_Depth AS (
    SELECT 
        service_count,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
        ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
    FROM customers
    GROUP BY service_count
)
SELECT 
    service_count,
    total_customers,
    churned_count,
    ROUND(churned_count * 100.0 / total_customers, 2) AS churn_rate_pct,
    avg_monthly_charges
FROM Service_Depth
ORDER BY service_count;

-- Expected Business Insight:
-- Confirms a dramatic inverse relationship between bundle depth and churn:
-- Single-service subscribers suffer an extreme 69.86% churn rate.
-- At 4 services, churn falls to 36.48%; at 6 services, churn is 25.55%;
-- At 8 services, churn falls to 12.41%; and at 9 services, churn is only 5.29%.
-- Multi-product bundling is the company's single most effective organic retention defense.


-- ------------------------------------------------------------------------------
-- QUERY 22: Window Function - DENSE_RANK() of Top Paying Subscribers by Contract
-- ------------------------------------------------------------------------------
-- Business Question:
-- Who are the top 3 highest-paying subscribers within each contract commitment type,
-- and are these premier revenue generators currently active or lost to churn?
--
-- Explanation of Logic:
-- Applies the `DENSE_RANK()` window function partitioned by `Contract` and ordered descending
-- by `MonthlyCharges`. Filters in the outer query for rank <= 3.

WITH Ranked_Subscribers AS (
    SELECT 
        customerID,
        Contract,
        MonthlyCharges,
        TotalCharges,
        Churn,
        DENSE_RANK() OVER (
            PARTITION BY Contract 
            ORDER BY MonthlyCharges DESC
        ) AS rank_in_contract
    FROM customers
)
SELECT 
    Contract,
    rank_in_contract,
    customerID,
    MonthlyCharges,
    TotalCharges,
    Churn
FROM Ranked_Subscribers
WHERE rank_in_contract <= 3
ORDER BY Contract, rank_in_contract;

-- Expected Business Insight:
-- Highlights that the #1 highest paying customer in Month-to-month contracts (customer 2302-ANTDP,
-- paying $117.45/month) has ALREADY CHURNED. Similarly, the #2 and #3 highest payers in One-year
-- contracts (8199-ZLLSA and 2889-FPWRM, paying >$117/mo) have churned, exposing high-value vulnerability.


-- ------------------------------------------------------------------------------
-- QUERY 23: Window Function - ROW_NUMBER() to Identify Longest-Tenured Churners
-- ------------------------------------------------------------------------------
-- Business Question:
-- Which departed subscribers had accumulated the longest tenure before churning across
-- broadband connection technologies?
--
-- Explanation of Logic:
-- Filters for churned accounts (`Churn = 'Yes'`), applies `ROW_NUMBER()` partitioned by
-- `InternetService` ordered descending by `tenure` and `TotalCharges`, isolating the top 3 per tier.

WITH Ranked_Churners AS (
    SELECT 
        customerID,
        InternetService,
        tenure,
        MonthlyCharges,
        TotalCharges,
        ROW_NUMBER() OVER (
            PARTITION BY InternetService 
            ORDER BY tenure DESC, TotalCharges DESC
        ) AS rn
    FROM customers
    WHERE Churn = 'Yes'
)
SELECT 
    InternetService,
    rn AS longest_tenure_rank,
    customerID,
    tenure AS tenure_months,
    MonthlyCharges,
    TotalCharges
FROM Ranked_Churners
WHERE rn <= 3
ORDER BY InternetService, rn;

-- Expected Business Insight:
-- Reveals severe long-term relationship breakdowns: Customer 2889-FPWRM churned after a full
-- 72 months (6 years) on Fiber optic after contributing $8,684.80 in lifetime revenue.
-- Customer 8580-QVLOC churned after 72 months on DSL ($6,440.25 lifetime revenue).
-- These indicate critical end-of-lifecycle contract renewal friction or unresolved service escalations.


-- ------------------------------------------------------------------------------
-- QUERY 24: Window Function - Running Total of Lifetime Revenue by Tenure Cohort
-- ------------------------------------------------------------------------------
-- Business Question:
-- What is the cumulative running total of lifetime revenue accrued as customer tenure matures
-- from Year 1 through Year 6?
--
-- Explanation of Logic:
-- Aggregates revenue by `tenure_group`, then applies `SUM() OVER (ORDER BY ... ROWS BETWEEN
-- UNBOUNDED PRECEDING AND CURRENT ROW)` to generate cumulative cumulative totals.

WITH Cohort_Revenue AS (
    SELECT 
        tenure_group,
        ROUND(SUM(TotalCharges), 2) AS cohort_revenue
    FROM customers
    GROUP BY tenure_group
)
SELECT 
    tenure_group,
    cohort_revenue,
    ROUND(SUM(cohort_revenue) OVER (
        ORDER BY tenure_group 
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total_revenue,
    ROUND(cohort_revenue * 100.0 / (SELECT SUM(TotalCharges) FROM customers), 2) AS pct_of_total_revenue
FROM Cohort_Revenue
ORDER BY tenure_group;

-- Expected Business Insight:
-- While Year 1 (0-12m) customers represent 31.0% of all accounts, they contribute only $601,651.90
-- (3.75% of cumulative revenue). In contrast, Year 6 customers (61-72m) generate $7,289,202.45
-- (45.40% of all company lifetime revenue), proving that preserving customers past Year 2 is where
-- massive enterprise value is created.


-- ------------------------------------------------------------------------------
-- QUERY 25: CTE & Composite Risk Scoring - Flight Risk Profiling
-- ------------------------------------------------------------------------------
-- Business Question:
-- How can subscribers be classified into an actionable 3-tier Flight Risk Scorecard
-- combining commitment length, network technology, payment channel, and tenure?
--
-- Explanation of Logic:
-- Builds a weighted composite risk score in CTE `Risk_Scoring`:
-- +3 points for Month-to-month contracts
-- +2 points for Fiber optic internet
-- +2 points for Electronic check payment
-- +2 points for tenure <= 12 months
-- Classifies into Critical Risk (Score 7-9), Moderate Risk (Score 4-6), Low Risk (Score 0-3).

WITH Risk_Scoring AS (
    SELECT 
        customerID,
        Contract,
        InternetService,
        PaymentMethod,
        tenure,
        MonthlyCharges,
        Churn,
        (CASE WHEN Contract = 'Month-to-month' THEN 3 ELSE 0 END +
         CASE WHEN InternetService = 'Fiber optic' THEN 2 ELSE 0 END +
         CASE WHEN PaymentMethod = 'Electronic check' THEN 2 ELSE 0 END +
         CASE WHEN tenure <= 12 THEN 2 ELSE 0 END) AS risk_score
    FROM customers
)
SELECT 
    CASE 
        WHEN risk_score >= 7 THEN '1. Critical Risk (Score 7-9)'
        WHEN risk_score BETWEEN 4 AND 6 THEN '2. Moderate Risk (Score 4-6)'
        ELSE '3. Low Risk (Score 0-3)'
    END AS risk_tier,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(MonthlyCharges), 2) AS monthly_revenue_at_stake
FROM Risk_Scoring
GROUP BY 
    CASE 
        WHEN risk_score >= 7 THEN '1. Critical Risk (Score 7-9)'
        WHEN risk_score BETWEEN 4 AND 6 THEN '2. Moderate Risk (Score 4-6)'
        ELSE '3. Low Risk (Score 0-3)'
    END
ORDER BY risk_tier;

-- Expected Business Insight:
-- The Critical Risk tier accurately isolates 1,915 subscribers experiencing a massive 59.32% churn rate
-- (1,136 churners). This segment alone puts $151,332.90 in monthly revenue directly on the line.
-- Retention campaigns must target this specific sub-population with automatic payment discounts
-- and annual contract migration incentives.


-- ------------------------------------------------------------------------------
-- QUERY 26: Relational JOIN Architecture - Normalized Dimension Analysis
-- ------------------------------------------------------------------------------
-- Business Question:
-- How can we query demographic vulnerability, contract commitment, and financial outcomes
-- across normalized relational tables using multi-table INNER JOINs?
--
-- Explanation of Logic:
-- Demonstrates multi-table relational join syntax between `fact_billing_churn`, `dim_contracts`,
-- and `dim_demographics` (or normalized CTE representations), focusing on month-to-month accounts.

SELECT 
    d.SeniorCitizen_Label,
    c.Contract,
    c.payment_category,
    COUNT(f.customerID) AS customer_count,
    ROUND(AVG(f.MonthlyCharges), 2) AS avg_monthly_charges,
    SUM(CASE WHEN f.Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN f.Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(f.customerID), 2) AS churn_rate_pct
FROM fact_billing_churn f
INNER JOIN dim_contracts c ON f.customerID = c.customerID
INNER JOIN dim_demographics d ON f.customerID = d.customerID
WHERE c.Contract = 'Month-to-month'
GROUP BY d.SeniorCitizen_Label, c.Contract, c.payment_category
ORDER BY churn_rate_pct DESC;

-- Expected Business Insight:
-- Demonstrates relational query performance and confirms that Senior Citizens on Month-to-month
-- contracts paying manually suffer the highest single churn rate in the entire company: 59.15% (346 churners
-- out of 585 subscribers), paying an average fee of $78.41/month.
