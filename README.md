# Customer Churn & Retention Intelligence System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Developer_Mode_(PBIP)-F2C811.svg)](https://powerbi.microsoft.com/)
[![Excel](https://img.shields.io/badge/Microsoft_Excel-Advanced_Modeling-217346.svg)](https://www.microsoft.com/excel)
[![Status](https://img.shields.io/badge/Status-Built_%26_User--Checked-blue.svg)]()

An enterprise-grade, end-to-end Data Analytics and Business Intelligence project engineered to diagnose customer attrition, quantify revenue exposure, and deploy targeted retention strategies for telecom subscribers. Built across **Microsoft Excel, Python (Pandas), MySQL 8.0, and Power BI (PBIP Developer Mode)**.

---

## 📌 Executive Summary & Key Results

Subscription businesses depend on recurring cash flow. In the IBM Telco dataset of **7,043 subscribers**, customer attrition represents severe financial leakage:

* **Total Active Base:** 7,043 customers generating **$456,116.60** in Monthly Recurring Revenue (MRR).
* **Total Churn Volume:** **1,869 customers lost** (**26.54% churn rate**).
* **Direct Revenue Leakage:** **$139,130.85 lost MRR** (30.50% of monthly revenue stream).
* **Cumulative Lifetime Loss:** **$2.86 Million** in historical billings lost.
* **Flight Risk Concentration:** A 4-variable heuristic risk model isolated **1,915 high-risk subscribers** (**59.32% churn rate**) holding **$151,332.90 in monthly revenue exposure**, responsible for **60.78% of all churned accounts**.

| Benchmark Metric | Retained Base | Churned Base | Overall / Variance |
| :--- | :---: | :---: | :---: |
| **Customer Count** | 5,174 (73.46%) | 1,869 (26.54%) | 7,043 |
| **Monthly Revenue (MRR)** | $316,985.75 | $139,130.85 | $456,116.60 |
| **Average Monthly Charges** | $61.27 / mo | $74.44 / mo | +$13.17 / mo (+21.5%) |
| **Average Customer Tenure** | 37.6 months | 18.0 months | -19.6 months (-52.1%) |
| **Average Lifetime Value (LTV)** | $2,549.91 | $1,531.80 | -$1,018.11 (-40.0%) |

---

## 🏗️ Architecture & Technology Stack

The project follows a structured data engineering and analytics lifecycle:

```mermaid
flowchart LR
    A["Raw Data (CSV)<br/>7,043 Rows × 21 Cols"] --> B["Phase 1: Data Audit<br/>Quality Profiling & Missing Values"]
    B --> C["Phase 2: Excel & Python<br/>ETL, Zero-Tenure Fix, 4 Features"]
    C --> D["Phase 3: MySQL 8.0<br/>3NF & Star Schema, 26 Queries"]
    D --> E["Phase 4: Power BI (PBIP)<br/>Semantic model, 29 DAX measures, 3 report pages"]
    E --> F["Executive Dashboard<br/>Interactive Retention Intelligence"]
```

| Layer | Technology | Key Capabilities & Deliverables |
| :--- | :--- | :--- |
| **Ingestion & Audit** | Excel & Python | Initial data profiling, data dictionary, anomaly detection, missing value audit. |
| **Data Cleaning** | Excel & Pandas | Non-destructive zero-tenure imputation ($0.00), data type enforcement, 4 engineered features. |
| **Relational Storage** | MySQL 8.0 | Dual-schema design (3NF relational and Star Schema dimensional), indexing, foreign keys. |
| **Analytical SQL** | MySQL 8.0 SQL | 26 production queries: window functions, CTEs, cohort analysis, revenue risk scoring. |
| **BI & Data Modeling** | Power BI Developer Mode | Folder-based `.pbip` project, `model.bim` (TMSL), M-query pipeline, 29 DAX measures. |
| **Dashboarding** | Power BI Visual Canvas | 3 interactive pages: Executive Overview, Churn Drivers, Revenue & Retention Intelligence. |

---

## 📂 Repository Structure

```text
Customer-Churn-Retention-Intelligence/
├── dataset/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Original raw dataset (7,043 × 21)
│   └── cleaned_telco_customer_churn.csv       # Production cleaned dataset (7,043 × 25)
├── documentation/
│   ├── DATA_UNDERSTANDING_AND_QUALITY_REPORT.md # Initial Phase 1 audit report
│   ├── DATA_CLEANING_REPORT.md                 # Cleaning methodology & audit trail
│   ├── PHASE_2_VERIFICATION.md                 # Excel & Python verification matrix
│   ├── MYSQL_DATABASE_DESIGN.md                # 3NF & Star Schema DDL specification
│   ├── SQL_DATA_VALIDATION_REPORT.md           # Benchmark query validation
│   ├── SQL_ANALYSIS_REPORT.md                  # Comprehensive findings across 26 queries
│   ├── PHASE_3_FINAL_VERIFICATION.md           # SQL architecture audit
│   ├── POWER_BI_DASHBOARD_REPORT.md            # DAX reference & visual specifications
│   ├── PROJECT_FINAL_VALIDATION_REPORT.md      # 53-check master validation report (100% PASS)
│   ├── BUSINESS_INSIGHTS_AND_STRATEGY.md       # Strategic executive playbooks
│   ├── INTERVIEW_QUESTIONS_AND_ANSWERS.md      # Placement & interview preparation guide
│   └── RESUME_PROJECT_DESCRIPTION.md           # Resume-ready bullet points & metrics
├── excel/
│   ├── raw_data.xlsx                           # Original dataset with validation rules
│   ├── cleaned_data.xlsx                       # Cleaned dataset formatted as Excel Table
│   ├── excel_analysis.xlsx                     # Formula-driven KPI summary & cross-tabs
│   └── data_quality_report.xlsx                # Automated data quality audit dashboard
├── powerbi/
│   ├── Customer_Churn_Dashboard.pbip           # Power BI Project root descriptor
│   ├── Customer_Churn_Dashboard.SemanticModel/ # Tabular semantic model
│   │   ├── definition.pbism                   # Semantic-model descriptor
│   │   └── model.bim                           # TMSL schema (columns, measures, M partition)
│   ├── Customer_Churn_Dashboard.Report/        # Report layout definition
│   │   ├── definition.pbir                     # Dataset reference binding
│   │   └── definition/                        # Modern PBIR report definition
│   ├── dax_measures.dax                        # Centralized DAX measures library (29 measures)
│   ├── power_query_transformations.m           # Standalone Power Query M script
│   ├── dashboard_page1_executive_overview.png  # Canvas mockup: Executive Overview
│   ├── dashboard_page2_churn_analysis.png      # Canvas mockup: Churn Driver Analysis
│   └── dashboard_page3_revenue_retention.png   # Canvas mockup: Revenue & Retention Intelligence
├── python/
│   ├── data_cleaning.py                        # Automated, repeatable ETL pipeline
│   ├── load_to_mysql.py                        # Automated MySQL loader & schema orchestrator
│   ├── generate_pbip.py                        # Programmatic PBIP project generator
│   └── validate_entire_project.py              # automated project validation suite
├── sql/
│   ├── 01_create_database.sql                  # Database initialization
│   ├── 02_create_tables.sql                    # 3NF & Star Schema DDL with constraints
│   ├── 03_load_data.sql                        # SQL data loading & verification checks
│   ├── 04_basic_analysis.sql                   # Basic queries & categorical distributions
│   ├── 05_churn_analysis.sql                   # Deep-dive churn driver queries
│   ├── 06_revenue_analysis.sql                 # Financial impact & ARPU analysis
│   └── 07_advanced_analysis.sql                # Advanced CTEs, window functions & scoring
├── .gitignore                                  # Git exclusion rules
├── requirements.txt                            # Python environment dependencies
└── README.md                                   # Master project documentation
```

---

## 🔍 Detailed Phase Breakdown

### Phase 1: Data Understanding & Data Quality Audit
* **Volume:** 7,043 customer accounts across 21 raw columns (demographics, services, billing, churn).
* **Missing Value Investigation:** Identified 11 blank strings in `TotalCharges`. All 11 accounts exhibited `tenure = 0` (brand-new accounts billed next cycle).
* **Integrity Validation:** 0 duplicate customer IDs, 0 native nulls in other columns, valid binary churn label (`Yes` / `No`).

### Phase 2: Excel & Python Cleaning & Feature Engineering
* **Non-Destructive Imputation:** Replaced 11 blank `TotalCharges` values strictly with `$0.00` for verified zero-tenure accounts.
* **Feature Engineering:**
  1. `SeniorCitizen_Label`: Transformed integer flags (0/1) into human-readable strings (`"Non-Senior"`, `"Senior Citizen"`).
  2. `tenure_group`: Grouped continuous tenure into 12-month cohorts (`0-12m`, `13-24m`, `25-36m`, `37-48m`, `49-60m`, `61-72m`).
  3. `payment_category`: Classified 4 payment methods into `"Automatic"` (Bank Transfer, Credit Card) vs `"Manual"` (Electronic Check, Mailed Check).
  4. `service_count`: Quantified bundled subscriptions across 6 add-on services (Online Security, Backup, Device Protection, Tech Support, Streaming TV, Streaming Movies).
* **Deliverables:** Built 4 standalone Excel workbooks and an automated Python ETL script (`python/data_cleaning.py`).

### Phase 3: Relational Architecture & Analytical SQL (MySQL 8.0)
* **Dual-Schema Design:**
  * **3NF Normalized Relational Model:** `customers` $\rightarrow$ `customer_services` $\rightarrow$ `customer_contracts` $\rightarrow$ `customer_billing`.
  * **Dimensional Star Schema:** Central fact table `fact_customer_churn` joined with dimensions `dim_customer`, `dim_contract`, `dim_services`, `dim_payment`.
* **Analytical Queries (26 Queries in 4 Modules):**
  * Evaluated churn rates across contract types (Month-to-month: 42.71% vs Two-year: 2.83%).
  * Quantified payment method attrition (Electronic Check churn: 45.29% driving $57.3K Lost MRR).
  * Cohort analysis using `DENSE_RANK()`, `NTILE(4)`, `COALESCE()`, and multi-table CTEs.
  * Formulated the Heuristic Flight Risk Tier scoring algorithm.

### Phase 4: Power BI Developer Mode (.pbip) & Executive Dashboard
* **Architecture:** Implemented using Microsoft Developer Mode (`.pbip`) format:
  * Semantic Model defined in `Customer_Churn_Dashboard.SemanticModel/model.bim` (TMSL JSON format).
  * Complete 3-page interactive report layout defined in `Customer_Churn_Dashboard.Report/report.json`.
  * Power Query transformations embedded directly in the import partition.
* **DAX Library (32 Measures across 4 folders):**
  * Core Volume (`Total Customers`, `Churned Customers`, `Churn Rate %`, `Retention Rate %`).
  * Financials (`Total Monthly Revenue (MRR)`, `Lost MRR`, `Retained MRR`, `Average Monthly Charges`, `LTV`).
  * Risk Intelligence (`Revenue at Risk`, `Realized Lost MRR (Critical)`, `Critical Risk Customer Count`, `Critical Risk Churn Rate %`).
* **3-Page Interactive Canvas:**
  1. **Executive Overview:** High-level executive KPI cards, churn distribution donut chart, contract churn rates, tenure volume, payment method loss.
  2. **Customer Churn Analysis:** Multi-dimensional driver matrix analyzing tenure, internet service, payment method, tech support, online security, and service bundling.
  3. **Revenue & Retention Intelligence:** Financial revenue at risk, risk-tier customer composition donut chart, lost MRR distributions, and strategic recommendations.

---

## 💡 Strategic Business Insights & Retention Playbooks

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TOP 4 ATTRITION VULNERABILITIES                                 │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Vulnerability Factor     │ Churn Rate & Exposure    │ Root Cause                       │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ 1. Month-to-Month Term   │ 42.71% Churn ($122.9K)   │ Zero switching cost, price shocks│
│ 2. First-Year Cohort     │ 47.44% Churn ($68.2K)    │ Poor early onboarding experience │
│ 3. Fiber Optic Internet  │ 41.89% Churn ($118.7K)   │ High ARPU ($91.50) without support│
│ 4. Electronic Check      │ 45.29% Churn ($57.3K)    │ Manual billing friction & fees   │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

### Actionable Retention Playbooks & Financial Opportunity Model
1. **Contract Migration Incentive:** Transition month-to-month subscribers to 12-month agreements by offering a **10% monthly discount or complimentary streaming add-on**. Converting 25% of retained month-to-month accounts preserves an estimated **$38,800/month ($465.6K ARR)**.
2. **First-Year Onboarding Cadence:** Trigger automated check-ins at **Day 14, 30, 60, and 90** for new subscribers. Proactive customer success reduces early churn by an estimated **15% ($10,230/mo saved, $122.8K ARR)**.
3. **Fiber Optic "Value Shield" Bundling:** Package **Tech Support and Online Security** into premium Fiber Optic tiers at no extra charge. Data proves subscribers with Tech Support churn at only **15.16%** vs **41.64%** without it, shielding an estimated **$47,800/mo ($573.6K ARR)**.
4. **Auto-Pay Migration Campaign:** Introduce a **$5/month statement credit** for transitioning from Electronic Check to Bank Draft or Credit Card Auto-Pay, removing monthly payment friction and shielding an estimated **$8,900/mo ($106.8K ARR)**.

> [!NOTE]
> **Financial Disclosure on Modeled Projections:**
> The **$1.27M annual revenue preservation figure is a forward-looking theoretical business case model**, not realized cash flow. The actual historical lost revenue is **$139,130.85/month ($1.67M ARR)**, and the active Monthly Recurring Revenue of retained Critical Flight Risk accounts is **$60,501.95/month ($726K ARR)**. Modeled savings assume 100% campaign target realization across the 5,174 active accounts. Conservative sensitivity modeling projects **$570,000/year ARR** at 50% target realization.

---

## ⚠️ Transparent Engineering & Verification Disclosures

In accordance with professional data engineering standards, testing boundaries are transparently documented:
1. **Power BI Project (.pbip) Architecture:** The `.pbip` project structure, Tabular Model (`model.bim` TMSL format v1567), dataset binding (`definition.pbidataset`), and report canvas layouts (`report.json` with 3 sections and 32 visuals) have been programmatically generated and structurally verified. However, **runtime visual rendering inside the Power BI Desktop GUI has not been independently observed by the automated agent** due to headless terminal sandbox boundaries. Users should open `powerbi/Customer_Churn_Dashboard.pbip` directly in Microsoft Power BI Desktop to inspect visual canvases.
2. **MySQL 8.0 Execution:** All DDL scripts, constraints, indexing, and 26 analytical SQL queries are strictly authored for MySQL 8.0 syntax. **Execution against a live MySQL server daemon has not been performed** in this environment because no active MySQL service was running on localhost port 3306. The scripts have been verified via relational SQL engine parsing and standalone Python validation. Production loading can be executed via `python python/load_to_mysql.py` once a live MySQL instance is connected.

## 🧪 Master Validation Results

The entire project is verified against a 45-point automated validation engine (`python/validate_entire_project.py`):

```text
======================================================================
MASTER VALIDATION SUMMARY: 45 / 45 CHECKS PASSED (100% PASS RATE)
======================================================================
[PASS] Dataset Row Count: 7,043 rows
[PASS] Dataset Column Count: 25 columns
[PASS] Unique Customer IDs: 7,043 (0 duplicates)
[PASS] Missing Values: 0 nulls across all fields
[PASS] Churned Customers: 1,869 accounts (26.54%)
[PASS] Retained Customers: 5,174 accounts (73.46%)
[PASS] Total Monthly Recurring Revenue (MRR): $456,116.60
[PASS] Lost MRR: $139,130.85 (30.50% loss)
[PASS] Zero-Tenure Imputation: 11 accounts verified at $0.00 TotalCharges
[PASS] Critical Flight Risk Tier: 1,915 customers | 59.32% churn | $151,332.90 exposure
[PASS] Excel Workbooks: 4/4 workbooks validated with active tables
[PASS] SQL Deliverables: 7/7 SQL files syntactically validated for MySQL 8.0
[PASS] Power BI PBIP Architecture: model.bim, report.json, definition files valid
[PASS] Power BI Canvas Configuration: 3 pages, 32 visuals, correct donut chart composition
======================================================================
```

*For complete validation logs, see [`documentation/PROJECT_FINAL_VALIDATION_REPORT.md`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/documentation/PROJECT_FINAL_VALIDATION_REPORT.md).*

---

## 🚀 Quickstart & Reproduction Guide

### Prerequisites
* Python 3.10 or higher
* Microsoft Power BI Desktop (June 2023 release or newer with Developer Mode enabled)
* Microsoft Excel 2016+
* MySQL Server 8.0 (Optional, for running SQL scripts directly against live database)

### Installation
```bash
# 1. Clone repository
git clone https://github.com/<your-username>/Customer-Churn-Retention-Intelligence.git
cd Customer-Churn-Retention-Intelligence

# 2. Set up virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Reproduce Data Cleaning & Validation
```bash
# Run data cleaning pipeline
python python/data_cleaning.py

# Run full project validation suite
python python/validate_entire_project.py
```

### Opening the Power BI Dashboard
1. Open **Microsoft Power BI Desktop**.
2. Go to **File $\rightarrow$ Open report $\rightarrow$ Browse reports**.
3. Navigate to `powerbi/Customer_Churn_Dashboard.pbip` and select it.
4. The semantic model, DAX measures, and all 3 visual canvas pages will automatically load.
5. If desired, click **File $\rightarrow$ Save As** and select **Power BI File (*.pbix)** to generate a compiled `.pbix` standalone file.

---

## 💼 Interview & Placement Readiness

* **Technical Interview Guide:** Comprehensive answers to 20+ core Data Analyst interview questions on SQL window functions, DAX evaluation contexts, data quality auditing, and retention modeling in [`documentation/INTERVIEW_QUESTIONS_AND_ANSWERS.md`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/documentation/INTERVIEW_QUESTIONS_AND_ANSWERS.md).
* **Resume Bullet Points:** Tailored bullet points with quantifiable business impact metrics for resume and LinkedIn integration in [`documentation/RESUME_PROJECT_DESCRIPTION.md`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/documentation/RESUME_PROJECT_DESCRIPTION.md).

---

## 📄 License & Attribution
This project is open-source under the [MIT License](LICENSE). Dataset provided by IBM Business Analytics Community.


## Validation and reproducibility notes

- The project includes a static validation report; its reported checks are not a substitute for running every workflow on another machine.
- The user opened the PBIP report in Power BI Desktop and checked all three report pages. Visual appearance and data refresh should still be rechecked after moving the project to another computer.
- MySQL scripts were prepared and syntax-reviewed, but a live MySQL server execution was not confirmed as part of this project validation.
- The customer risk score is a rule-based heuristic, not a trained machine-learning prediction model.
- The Power BI model's data-source path may need to be updated to the location of `dataset/cleaned_telco_customer_churn.csv` on your computer.
