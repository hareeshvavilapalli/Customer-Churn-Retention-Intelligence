-- ==============================================================================
-- Project: Customer Churn & Retention Intelligence System
-- Script: 05_churn_analysis.sql
-- Description: Driver analysis isolating contract, tenure, payment, and service churn factors
-- Target RDBMS: MySQL 8.0+
-- Author: Senior Data Analyst
-- ==============================================================================

USE customer_churn_db;

-- ------------------------------------------------------------------------------
-- QUERY 7: Churn Rate by Contract Commitment Type
-- ------------------------------------------------------------------------------
-- Business Question:
-- What is the exact customer churn rate across each contract commitment type,
-- and what share of total company churn originates from month-to-month contracts?
--
-- Explanation of Logic:
-- Groups by `Contract` and computes total subscribers, retained count, churn count,
-- segment churn rate, and the proportion of the company's total churn pool (1,869 churners).

SELECT 
    Contract,
    COUNT(*) AS total_subscribers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_subscribers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_subscribers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / (SELECT SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) FROM customers), 2) AS share_of_total_churn_pct
FROM customers
GROUP BY Contract
ORDER BY churned_subscribers DESC;

-- Expected Business Insight:
-- Contract commitment is the single strongest determinant of customer churn. Month-to-month
-- subscribers experience a 42.71% churn rate, accounting for 1,655 out of 1,869 churners (88.55%
-- of all churn). In contrast, Two-year contract holders churn at an ultra-low 2.83%.


-- ------------------------------------------------------------------------------
-- QUERY 8: Customer Lifecycle & Tenure Cohort Churn Rates
-- ------------------------------------------------------------------------------
-- Business Question:
-- At what stage in the customer lifecycle does subscriber attrition peak,
-- and how does churn risk evolve as tenure matures?
--
-- Explanation of Logic:
-- Groups by the engineered `tenure_group` cohorts (0-12m, 13-24m, 25-36m, 37-48m, 49-60m, 61-72m)
-- and computes segment churn rates and cumulative churn contributions.

SELECT 
    tenure_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / (SELECT SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) FROM customers), 2) AS share_of_total_churn_pct
FROM customers
GROUP BY tenure_group
ORDER BY tenure_group;

-- Expected Business Insight:
-- Customer churn is severely front-loaded: 55.48% of all churn (1,037 churners) occurs during
-- the first 12 months of service (churn rate: 47.44%). By Year 5 and 6 (49-72 months), churn
-- drops precipitously to 14.42% and 6.61%, proving that long-tenured customers become sticky.


-- ------------------------------------------------------------------------------
-- QUERY 9: Churn Rate by Payment Method & Billing Friction Category
-- ------------------------------------------------------------------------------
-- Business Question:
-- Which payment settlement methods experience the highest attrition, and how does manual
-- payment friction compare against automated bank/card withdrawals?
--
-- Explanation of Logic:
-- Groups by `PaymentMethod` and the engineered `payment_category` ('Automatic' vs 'Manual')
-- to contrast billing automation against customer retention.

SELECT 
    PaymentMethod,
    payment_category,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod, payment_category
ORDER BY churn_rate_pct DESC;

-- Expected Business Insight:
-- Electronic check users suffer a staggering 45.29% churn rate (1,071 churners out of 2,365 users).
-- Conversely, automated methods (Bank transfer: 16.71%, Credit card: 15.24%) have one-third the churn rate,
-- confirming that manual invoicing introduces repeated friction and payment failure opportunities.


-- ------------------------------------------------------------------------------
-- QUERY 10: Broadband Technology (Fiber Optic vs DSL vs None)
-- ------------------------------------------------------------------------------
-- Business Question:
-- How does subscriber churn vary across broadband connection technologies,
-- and what role does monthly pricing play?
--
-- Explanation of Logic:
-- Groups by `InternetService`, calculating subscriber volumes, retained vs churned headcounts,
-- segment churn rates, and average monthly fees.

SELECT 
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;

-- Expected Business Insight:
-- Fiber optic internet exhibits an alarming 41.89% churn rate (1,297 churners out of 3,096 subscribers)
-- at an average fee of $91.50/mo. DSL churn is much lower at 18.96% ($58.10/mo), and No Internet is 7.40%.
-- High Fiber churn points to price-to-value dissatisfaction or service outage friction.


-- ------------------------------------------------------------------------------
-- QUERY 11: Impact of Online Security and Tech Support on Churn
-- ------------------------------------------------------------------------------
-- Business Question:
-- Do cybersecurity protection and priority technical support protect against customer departure?
--
-- Explanation of Logic:
-- Cross-tabulates `OnlineSecurity` and `TechSupport` subscriptions to isolate the retention uplift
-- generated by essential technical safeguards.

SELECT 
    OnlineSecurity,
    TechSupport,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY OnlineSecurity, TechSupport
ORDER BY churn_rate_pct DESC;

-- Expected Business Insight:
-- Customers who lack both Online Security and Tech Support suffer an extreme 50.19% churn rate.
-- Having both services cuts the churn rate to just 9.53%—a retention improvement of more than
-- 40 percentage points, demonstrating the high strategic value of security/support bundles.


-- ------------------------------------------------------------------------------
-- QUERY 12: Invoicing Preference & Paperless Billing Impact
-- ------------------------------------------------------------------------------
-- Business Question:
-- How does digital e-invoicing (Paperless Billing) influence customer churn?
--
-- Explanation of Logic:
-- Groups by `PaperlessBilling` and computes churn counts, churn percentages, and average monthly charges.

SELECT 
    PaperlessBilling,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM customers
GROUP BY PaperlessBilling;

-- Expected Business Insight:
-- Customers opted into Paperless Billing churn at more than double the rate of paper invoice users
-- (33.57% vs 16.33%). Paperless billing correlates with higher monthly charges ($74.44 vs $51.27)
-- and electronic payment channels, which amplify billing sensitivity.


-- ------------------------------------------------------------------------------
-- QUERY 13: Entertainment Streaming Services Churn Impact
-- ------------------------------------------------------------------------------
-- Business Question:
-- Does subscribing to TV and Movie streaming services reduce churn or inflate monthly bills?
--
-- Explanation of Logic:
-- Groups by `StreamingTV` and `StreamingMovies` combinations, tracking customer counts, churn rates,
-- and average monthly billing.

SELECT 
    StreamingTV,
    StreamingMovies,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM customers
GROUP BY StreamingTV, StreamingMovies
ORDER BY customer_count DESC;

-- Expected Business Insight:
-- Bundling both Streaming TV and Movies drives ARPU to an average of $94.40/mo, but maintains
-- a 29.89% churn rate. Unlike Tech Support, entertainment add-ons do not inherently anchor
-- retention unless paired with long-term contracts.
