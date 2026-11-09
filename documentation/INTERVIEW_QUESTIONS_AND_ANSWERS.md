# Data Analyst Technical Interview Preparation Guide
**Project:** Customer Churn & Retention Intelligence System  
**Audience:** Hiring Managers, Technical Interviewers, Campus Placement Panels  
**Candidate Role:** Senior Data Analyst / BI Analyst  

---

## 📌 Section 1: Project Overview & Executive Presentation

### Q1: Can you walk me through an end-to-end data analytics project you recently built?
**Ideal Answer:**
"I designed and deployed the **Customer Churn & Retention Intelligence System**, analyzing 7,043 telecom subscribers to diagnose customer attrition, quantify revenue exposure, and build proactive retention strategies. 

The project spans four distinct engineering and analytical tiers:
1. **Data Ingestion & Quality Audit (Excel & Python):** Profiled 21 raw features, identified and resolved 11 missing TotalCharges records strictly tied to new accounts (`tenure = 0`), and engineered 4 business features.
2. **Relational Database Design & Analytical SQL (MySQL 8.0):** Built a normalized 3NF database and a Star Schema dimensional warehouse. Authored 26 analytical SQL queries utilizing CTEs, window functions (`DENSE_RANK`, `NTILE`), and cohort aggregates.
3. **Power BI Developer Mode (PBIP) & DAX Modeling:** Programmatically engineered a Tabular Semantic Model (`model.bim`) with 32 DAX measures, dynamic Power Query M partitioning, and a 3-page executive reporting canvas.
4. **Strategic Business Intelligence:** Formulated a 4-variable heuristic flight risk model that isolated 1,915 critical-risk accounts holding $151,332.90 in monthly revenue exposure, delivering 4 actionable retention playbooks capable of preserving $1.27M in annual revenue."

### Q2: Why did you choose this business problem, and what makes customer churn critical?
**Ideal Answer:**
"In recurring-revenue subscription businesses (SaaS, telecom, utilities), acquiring a new customer costs 5 to 7 times more than retaining an existing one. In our dataset, customer attrition was running at **26.54% (1,869 customers lost)**, draining **$139,130.85 every month in lost MRR**—over 30% of monthly revenues. Crucially, churned subscribers had an average monthly bill of $74.44 versus $61.27 for retained subscribers. Losing our highest-paying accounts is catastrophic for Customer Lifetime Value (LTV), making churn prevention the highest-ROI analytics initiative for management."

---

## 📌 Section 2: Data Cleaning, Quality Auditing & Excel / Python

### Q3: You discovered 11 blank values in TotalCharges. How did you investigate and handle them, and why didn't you simply drop or mean-impute them?
**Ideal Answer:**
"During initial profiling, `TotalCharges` appeared as a text column rather than a float because 11 records contained space characters (`' '`). 

Rather than blindly dropping records or imputing the mean—which would distort distributions—I investigated the underlying business logic:
* Every single one of the 11 blank records had `tenure = 0`.
* A tenure of 0 indicates brand-new customers who signed up during the current billing cycle and have not yet received their first monthly bill.
* Since no billing cycle had elapsed, their true historical cumulative spend is legitimately **$0.00**.

Imputing the dataset average (~$2,280) would have fabricated non-existent revenue. Dropping them would discard valuable active customers. Therefore, I programmatically imputed `$0.00` strictly for verified zero-tenure records and cast the field to a floating-point numeric type. This preserved all 7,043 customer accounts with zero data loss."

### Q4: How did you ensure data integrity between your Excel workbooks and your Python pipeline?
**Ideal Answer:**
"I implemented automated cross-validation tests. In Python, I built an automated verification suite (`python/validate_entire_project.py`) that evaluated row counts, unique Customer IDs, null counts, total MRR ($456,116.60), and cumulative charges ($16,056,168.70). In Excel, I utilized structured Excel Tables (`Table1`) with formulas like `COUNTIF`, `SUMIFS`, `AVERAGEIFS`, and `IFERROR`, verifying that both engines returned matching aggregations to the exact cent."

---

## 📌 Section 3: Relational Architecture & MySQL 8.0 SQL

### Q5: Explain your database schema design. Why did you implement both a 3NF relational schema and a Star Schema?
**Ideal Answer:**
"In enterprise architectures, transactional processing (OLTP) and analytical processing (OLAP) serve different objectives:
1. **Third Normal Form (3NF):** Designed for transactional integrity and eliminating redundancy. I decomposed the 25 flat attributes into four relational tables: `customers`, `customer_services`, `customer_contracts`, and `customer_billing`, enforced by foreign key constraints and primary keys on `customer_id`.
2. **Star Schema:** Optimized for analytical querying, aggregations, and BI ingestion. I built a central fact table, `fact_customer_churn`, surrounded by dimension tables (`dim_customer`, `dim_contract`, `dim_services`, `dim_payment`). This architecture minimizes complex joins for BI queries, speeds up slicing and dicing, and mirrors modern data warehouse standards like Snowflake or Databricks."

### Q6: Can you give an example of an advanced SQL query you wrote and explain the window functions used?
**Ideal Answer:**
"In `sql/07_advanced_analysis.sql`, I engineered a customer cohort ranking query to segment high-ARPU churn risks within each tenure cohort:
```sql
SELECT 
    customer_id,
    tenure_group,
    monthly_charges,
    DENSE_RANK() OVER (
        PARTITION BY tenure_group 
        ORDER BY monthly_charges DESC
    ) AS arpu_rank_within_cohort,
    NTILE(4) OVER (
        ORDER BY monthly_charges DESC
    ) AS spending_quartile
FROM fact_customer_churn
WHERE churn = 'Yes';
```
* `PARTITION BY tenure_group` resets the ranking across each 12-month tenure cohort.
* `DENSE_RANK()` assigns contiguous rank numbers without skipping values in the case of ties.
* `NTILE(4)` divides the entire churn population into quartiles based on monthly spend, allowing marketing to identify the top 25% highest-spending departed accounts for win-back campaigns."

### Q7: In your SQL scripts, you included transaction controls and foreign key checks. Why was that necessary?
**Ideal Answer:**
"When executing batch table truncations or reloads in MySQL, tables with foreign key references throw `ERROR 1701: Cannot truncate a table referenced in a foreign key constraint`. To guarantee atomic, idempotent execution without breaking referential integrity, I wrapped table setup in:
```sql
SET FOREIGN_KEY_CHECKS = 0;
-- DDL & Truncations
SET FOREIGN_KEY_CHECKS = 1;
```
Additionally, in the Python MySQL loader (`python/load_to_mysql.py`), I utilized transaction blocks with `connection.commit()` and `connection.rollback()` inside `try...except` blocks to ensure that if any batch failed, the database remained in a clean, consistent state."

---

## 📌 Section 4: Power BI, DAX & Power BI Developer Mode (PBIP)

### Q8: What is Power BI Developer Mode (.pbip), and why did you use it instead of saving a binary .pbix?
**Ideal Answer:**
"Traditionally, Power BI reports are compiled into proprietary binary `.pbix` files, which are opaque black boxes incompatible with Git version control, CI/CD pipelines, and multi-developer collaboration. 

Microsoft introduced **Power BI Developer Mode (`.pbip`)**, which decomposes the project into plain-text JSON and TMDL files:
* `Customer_Churn_Dashboard.SemanticModel`: Contains `model.bim` (TMSL JSON) defining the schema, relationships, partitions, and all DAX measures.
* `Customer_Churn_Dashboard.Report`: Contains `report.json` defining the canvas layout, visual containers, charts, and slicers.

By generating the `.pbip` project programmatically using Python:
1. The entire dashboard is 100% version-controllable in Git with clean text diffs.
2. DAX measures and visual layouts can be automated and audited.
3. Anyone cloning the repository can open `Customer_Churn_Dashboard.pbip` directly in Power BI Desktop with zero manual setup."

### Q9: What is the difference between an Implicit Measure and an Explicit Measure in Power BI, and which did you use?
**Ideal Answer:**
"An **implicit measure** occurs when an analyst drags a raw numeric column (like `MonthlyCharges`) into a visual card and lets Power BI default to `Sum of MonthlyCharges`. This is poor practice because implicit measures cannot be referenced by other calculations, are difficult to maintain, and behave unpredictably in complex filter contexts.

An **explicit measure** is a user-defined DAX expression, such as:
```dax
Total Monthly Revenue (MRR) = SUM('CustomerChurn'[MonthlyCharges])
```
I authored **32 explicit DAX measures** organized into structured display folders (`1. Volume & Churn`, `2. Financial & Revenue`, `3. Risk Intelligence`, `4. Segment Losses`). Explicit measures allow clean nesting (e.g. `DIVIDE([Churned Customers], [Total Customers], 0)`), apply consistent formatting strings, and respect row-level and filter-context modifications across all visuals."

### Q10: Explain the DAX formula you created for 'Lost MRR' and how CALCULATE modifies the filter context.
**Ideal Answer:**
"The formula is:
```dax
Lost MRR = 
CALCULATE(
    SUM('CustomerChurn'[MonthlyCharges]),
    'CustomerChurn'[Churn] = "Yes"
)
```
`CALCULATE` is the most powerful function in DAX because it transitions row context into filter context and modifies existing filter context. Here, `CALCULATE` evaluates the sum of `MonthlyCharges` while overriding or adding a filter condition where `'CustomerChurn'[Churn]` must equal `'Yes'`. If a user filters by `Contract = "Month-to-month"` on the report canvas, `CALCULATE` intersects both filters, returning the exact lost revenue for month-to-month subscribers."

---

## 📌 Section 5: Business Sense, Analytics & Stakeholder Value

### Q11: Explain your Heuristic Flight Risk Tier model. Why heuristic rather than machine learning?
**Ideal Answer:**
"In analytics, transparency and business explainability often outweigh black-box complexity—especially when introducing risk scoring to operational teams. 

I formulated a heuristic risk scoring algorithm based on the four highest-odds attrition factors identified during SQL and EDA:
1. **Month-to-month contract:** +3 points (42.7% baseline churn).
2. **Fiber optic internet:** +2 points (41.9% churn, high ARPU).
3. **Electronic check payment:** +2 points (45.3% churn).
4. **Tenure $\le$ 12 months:** +2 points (47.4% churn).

Accounts scoring $\ge 7$ were classified as **Critical Flight Risk (1,915 customers)**. This heuristic model captured **60.78% of all churned accounts** with an empirical cohort churn rate of **59.32%**, isolating **$151,332.90 in monthly revenue exposure**. Frontline customer success representatives can instantly understand *why* an account is flagged (e.g. 'Month-to-month + Fiber + Electronic Check'), making retention interventions far more intuitive."

### Q12: If executive leadership gave you $100,000 to reduce churn over the next quarter, where would you allocate it?
**Ideal Answer:**
"I would allocate the $100,000 budget across two high-impact initiatives:
1. **$60,000 to a Month-to-Month Annual Contract Incentive:**
   Month-to-month contracts account for **$122,892.40/month in lost MRR (88.3% of all losses)**. I would offer a $10/month statement credit or complimentary premium service upgrade for switching to a 12-month agreement. Converting just 500 subscribers preserves **$35,000/month ($420,000 ARR)**, delivering a 4.2x ROI in year one.
2. **$40,000 to Automated Day 14/30/60 First-Year Onboarding & Tech Support Bundling:**
   Over **55% of churn happens in months 0–12**, particularly among Fiber Optic subscribers lacking Tech Support. Providing free automated setup check-ins and free 90-day Tech Support shields vulnerable accounts during the initial period where churn peaks at 47.4%."
