# PHASE 1: DATA UNDERSTANDING & DATA QUALITY AUDIT REPORT
**Project:** Customer Churn & Retention Intelligence System  
**Dataset:** IBM Telco Customer Churn (`dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv`)  
**Technology Stack:** Excel | Python (Pandas) | MySQL | Power BI  
**Author:** Senior Data Analyst  
**Audit Date:** November 8, 2026  
**Status:** Audit Complete — Awaiting Approval for Phase 2  

---

## 1. Executive Summary

A comprehensive data quality audit and structural inspection was performed on the raw IBM Telco Customer Churn dataset. The objective of this phase is to establish a rigorous baseline understanding of data health, identify schema flaws, analyze distribution properties, detect anomalies, and formulate an enterprise-grade data cleaning specification before downstream transformation across Python, MySQL, Excel, and Power BI.

### Key Audit Findings at a Glance
| Metric | Value | Analytical Assessment |
| :--- | :--- | :--- |
| **Total Record Count** | 7,043 rows | Zero truncated rows; complete transactional sample |
| **Total Column Count** | 21 columns | 1 Identifier, 4 Demographics, 9 Services, 3 Account/Billing, 3 Financial/Target |
| **Primary Key Integrity** | 100% Unique | 0 duplicate Customer IDs; format conforms strictly to `^\d{4}-[A-Z]{5}$` |
| **Row Duplicate Count** | 0 rows | No exact or near-identical record duplicates |
| **Missing Values (Null / NaN)**| 0 records | Zero native nulls detected across all columns |
| **Hidden Whitespace Missingness**| 11 records (0.156%) | In `TotalCharges` column; whitespace string `" "` masking missing values |
| **Root Cause of Missingness**| Deterministic / MNAR | All 11 cases correspond to **new customers** with `tenure = 0` |
| **Type Discrepancies** | 2 columns | `TotalCharges` stored as `object` (string); `SeniorCitizen` stored as `int64` (0/1) |
| **Outliers / Impossible Values**| 0 severe anomalies | No negative tenure, negative charges, or impossible billing values |
| **Overall Baseline Churn Rate** | **26.54%** (1,869 / 7,043)| Significant class imbalance (~2.77:1); high churn in 1st year (47.44%) |
| **Monthly Revenue at Risk (MRR)**| **$139,130.85** | Churned customers represent **30.50%** of total monthly recurring revenue |

---

## 2. Dataset Architecture & Dimensions

The dataset consists of **7,043 rows** and **21 columns**, representing individual telecom subscribers, their account configurations, demographic profiles, subscribed services, financial commitments, and customer churn status.

- **Total Dimensions:** 7,043 rows × 21 columns
- **Memory Footprint (Raw In-Memory):** ~1.15 MB
- **File Format:** Comma-Separated Values (CSV), UTF-8 encoded
- **Granularity:** One record per unique customer account (`customerID`)

---

## 3. Comprehensive Data Dictionary (All 21 Columns)

The 21 features are organized into four functional business domains:

### A. Customer Demographics & Identity (5 Columns)
| Column Name | Raw CSV Type | Recommended Type | Nulls | Cardinality | Distinct Values / Range | Business Definition & Analytical Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `customerID` | `object` | `VARCHAR(10)` | 0 | 7,043 | Alphanumeric (`0002-ORFBO` to `9995-HOTOH`) | Unique alphanumeric identifier for each customer. Primary key for entity resolution and SQL joining. |
| `gender` | `object` | `VARCHAR(6)` | 0 | 2 | `Male` (3,555; 50.48%), `Female` (3,488; 49.52%) | Customer gender. Used for demographic parity and segmentation. |
| `SeniorCitizen`| `int64` | `TINYINT` / `VARCHAR(3)`| 0 | 2 | `0` (Non-Senior: 5,977; 84.86%), `1` (Senior: 1,066; 15.14%) | Binary indicator whether subscriber is a senior citizen. Significant risk factor for churn. |
| `Partner` | `object` | `VARCHAR(3)` | 0 | 2 | `Yes` (3,402; 48.30%), `No` (3,641; 51.70%) | Indicates whether the customer has a domestic partner. Indicator of household stability. |
| `Dependents` | `object` | `VARCHAR(3)` | 0 | 2 | `No` (4,933; 70.04%), `Yes` (2,110; 29.96%) | Indicates whether customer lives with dependents (children, elderly relatives). High retention anchor. |

### B. Subscribed Services & Product Portfolio (9 Columns)
| Column Name | Raw CSV Type | Recommended Type | Nulls | Cardinality | Distinct Values / Breakdown | Business Definition & Analytical Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `PhoneService` | `object` | `VARCHAR(3)` | 0 | 2 | `Yes` (6,361; 90.32%), `No` (682; 9.68%) | Core voice line subscription status. |
| `MultipleLines`| `object` | `VARCHAR(16)`| 0 | 3 | `No` (3,390), `Yes` (2,971), `No phone service` (682) | Multi-line voice capability; hierarchical dependency on `PhoneService`. |
| `InternetService`| `object` | `VARCHAR(11)`| 0 | 3 | `Fiber optic` (3,096; 43.96%), `DSL` (2,421; 34.37%), `No` (1,526; 21.67%) | Core data connectivity technology. Primary driver of ARPU and customer churn. |
| `OnlineSecurity`| `object` | `VARCHAR(19)`| 0 | 3 | `No` (3,498), `Yes` (2,019), `No internet service` (1,526) | Cybersecurity add-on product. Crucial retention driver. |
| `OnlineBackup` | `object` | `VARCHAR(19)`| 0 | 3 | `No` (3,088), `Yes` (2,429), `No internet service` (1,526) | Cloud storage/backup add-on service. |
| `DeviceProtection`| `object`| `VARCHAR(19)`| 0 | 3 | `No` (3,095), `Yes` (2,422), `No internet service` (1,526) | Hardware warranty / tech insurance plan. |
| `TechSupport` | `object` | `VARCHAR(19)`| 0 | 3 | `No` (3,473), `Yes` (2,044), `No internet service` (1,526) | Priority technical support tier. Key customer satisfaction metric. |
| `StreamingTV` | `object` | `VARCHAR(19)`| 0 | 3 | `No` (2,810), `Yes` (2,707), `No internet service` (1,526) | IPTV streaming entitlement over telco network. |
| `StreamingMovies`| `object`| `VARCHAR(19)`| 0 | 3 | `No` (2,785), `Yes` (2,732), `No internet service` (1,526) | Movie streaming entitlement / VOD package. |

### C. Account, Contract & Billing Metadata (3 Columns)
| Column Name | Raw CSV Type | Recommended Type | Nulls | Cardinality | Distinct Values / Breakdown | Business Definition & Analytical Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Contract` | `object` | `VARCHAR(14)`| 0 | 3 | `Month-to-month` (3,875; 55.02%), `Two year` (1,695; 24.07%), `One year` (1,473; 20.91%) | Commitment term. Strongest predictor of subscriber retention. |
| `PaperlessBilling`| `object`| `VARCHAR(3)` | 0 | 2 | `Yes` (4,171; 59.22%), `No` (2,872; 40.78%) | Digital invoicing opt-in. Correlated with digital payment channels. |
| `PaymentMethod`| `object` | `VARCHAR(25)`| 0 | 4 | `Electronic check` (2,365; 33.58%), `Mailed check` (1,612; 22.89%), `Bank transfer (auto)` (1,544; 21.92%), `Credit card (auto)` (1,522; 21.61%) | Payment settlement channel. Automated vs manual billing friction. |

### D. Financial Metrics & Target Variable (4 Columns)
| Column Name | Raw CSV Type | Recommended Type | Nulls | Cardinality | Range / Summary Stats | Business Definition & Analytical Role |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `tenure` | `int64` | `SMALLINT` | 0 | 73 | Min: `0`, Max: `72` months (Mean: 32.37, Median: 29) | Total months customer has subscribed. Baseline for customer lifecycle. |
| `MonthlyCharges`| `float64`| `DECIMAL(10,2)`| 0 | 1,585 | Min: `$18.25`, Max: `$118.75` (Mean: $64.76, Median: $70.35) | Monthly recurring billing amount charged to customer. |
| `TotalCharges` | `object` | `DECIMAL(10,2)`| 11 blank | 6,531 | Min: `$18.80`, Max: `$8684.80` (Mean: $2283.30, Median: $1397.48) | Cumulative lifetime billing across tenure. Stored incorrectly as text. |
| `Churn` | `object` | `VARCHAR(3)` | 0 | 2 | `No` (5,174; 73.46%), `Yes` (1,869; 26.54%) | **Primary Project Target Variable**: Customer departure within the last billing cycle. |

---

## 4. Data Quality Audit Findings

### 4.1 Missing Values Analysis
- Standard programmatic null checks (`isna()`, `isnull()`, `NULL`) return **0 missing values** across all 21 columns.
- However, scanning for blank string representations (`" "`, `""`) discovered **11 records in the `TotalCharges` column** containing single space whitespace characters (`" "`).
- **Missingness Rate:** $11 / 7,043 = 0.156\%$.
- No other column exhibits whitespace, nulls, or placeholder tokens (such as `N/A`, `NULL`, `?`, or `-999`).

### 4.2 Duplicate Customer IDs & Row Redundancy
- **Unique Customer IDs:** Exactly 7,043 unique IDs across 7,043 rows.
- **Duplicate Customer ID Count:** **0**.
- **Full Row Duplicate Count:** **0**.
- **Primary Key Integrity:** Confirmed 100% compliant. Can safely serve as the primary key constraint in MySQL table DDL.

### 4.3 Data Type Inconsistencies & Structural Flaws
1. **`TotalCharges` (Object vs Float/Decimal):**
   - **Flaw:** Because 11 rows contain whitespace strings `" "`, Pandas inferred the column type as `object` (string).
   - **Impact:** Cannot perform mathematical operations, aggregations (`SUM`, `AVG`), or numerical sorting without explicit casting.
   - **Required Remediation:** Convert whitespace to `0.00` or numeric `NaN`, then cast column to `DECIMAL(10,2)` in MySQL, `float64` in Pandas, and `Decimal Number` in Power BI.
2. **`SeniorCitizen` (Integer Flag vs Boolean String):**
   - **Flaw:** Coded as numeric `0` and `1`, while all other boolean-style demographic features (`Partner`, `Dependents`, `PhoneService`, `PaperlessBilling`, `Churn`) are coded as `'Yes'` and `'No'`.
   - **Impact:** Causes inconsistency in Power BI slicers and filters where end users expect uniform `Yes`/`No` labels.
   - **Required Remediation:** Create an aliased representation (`Yes`/`No`) for business dashboards while maintaining binary `1/0` for analytical SQL/ML routines.

### 4.4 Inconsistent Categorical Values & Semantic Checks
- **Whitespace & Padding:** Categorical columns were evaluated for leading or trailing whitespace (`.str.strip() != .str`). **Zero whitespace padding errors detected.**
- **Casing & Spelling:** Standardized PascalCase across all categories; no typos (e.g., no `fiber optic` vs `Fiber optic`).
- **Hierarchical Service Dependencies:**
  - Phone dependency: 682 customers have `PhoneService = 'No'`. In `MultipleLines`, all 682 records strictly read `'No phone service'`.
  - Internet dependency: 1,526 customers have `InternetService = 'No'`. Across all six add-on columns (`OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`), all 1,526 records strictly read `'No internet service'`.
  - **Integrity Result:** Cross-service consistency is **100% structurally coherent**.

---

## 5. In-Depth Investigation: `TotalCharges` & `tenure`

A dedicated audit was conducted into the relationship between tenure, monthly fees, and lifetime billing:

### 5.1 The `tenure = 0` Anomaly
Detailed inspection of the 11 records containing blank `TotalCharges` revealed an exact, 1-to-1 relationship with `tenure = 0`:

```
Are blank TotalCharges records strictly identical to tenure == 0? -> TRUE (11 of 11)
```

#### Complete Profile of the 11 Anomalous Records:
| Row Index | Customer ID | Gender | Senior | Partner | Dependents | Tenure | Contract | Payment Method | Monthly Charges | Raw TotalCharges | Churn |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 488 | `4472-LVYGI` | Female | 0 | Yes | Yes | 0 | Two year | Bank transfer (auto) | $52.55 | `" "` | No |
| 753 | `3115-CZMZD` | Male | 0 | No | Yes | 0 | Two year | Mailed check | $20.25 | `" "` | No |
| 936 | `5709-LVOEQ` | Female | 0 | Yes | Yes | 0 | Two year | Mailed check | $80.85 | `" "` | No |
| 1082 | `4367-NUYAO` | Male | 0 | Yes | Yes | 0 | Two year | Mailed check | $25.75 | `" "` | No |
| 1340 | `1371-DWPAZ` | Female | 0 | Yes | Yes | 0 | Two year | Credit card (auto) | $56.05 | `" "` | No |
| 3331 | `7644-OMVMY` | Male | 0 | Yes | Yes | 0 | Two year | Mailed check | $19.85 | `" "` | No |
| 3826 | `3213-VVOLG` | Male | 0 | Yes | Yes | 0 | Two year | Mailed check | $25.35 | `" "` | No |
| 4380 | `2520-SGTTA` | Female | 0 | Yes | Yes | 0 | Two year | Mailed check | $20.00 | `" "` | No |
| 5218 | `2923-ARZLG` | Male | 0 | Yes | Yes | 0 | One year | Mailed check | $19.70 | `" "` | No |
| 6670 | `4075-WKNIU` | Female | 0 | Yes | Yes | 0 | Two year | Mailed check | $73.35 | `" "` | No |
| 6754 | `2775-SEFEE` | Male | 0 | No | Yes | 0 | Two year | Bank transfer (auto) | $61.90 | `" "` | No |

#### Critical Business Observations:
1. **Contract Type:** 10 of the 11 customers are on **Two year** contracts, and 1 is on a **One year** contract. None are Month-to-month.
2. **Dependents & Partners:** 9 of the 11 have Partners, and all 11 have Dependents. These are stable family households signing long-term commitments.
3. **Churn Status:** 100% of these 11 customers have `Churn = 'No'`.
4. **Business Interpretation:** These customers signed up within the current, unbilled cycle (tenure = 0 completed months). Because no monthly billing statement has closed yet, their cumulative historical bill (`TotalCharges`) is officially `$0.00`. The upstream source system exported an empty string rather than zero.

### 5.2 Mathematical Coherence: `TotalCharges` vs `(tenure × MonthlyCharges)`
For customers with `tenure > 0`, we evaluated the ratio $R = \frac{\text{TotalCharges}}{\text{tenure} \times \text{MonthlyCharges}}$:
- **For `tenure = 1`:** Exactly **613 out of 613 customers (100.0%)** have $\text{TotalCharges} = \text{MonthlyCharges}$ with an absolute delta of $\$0.000$.
- **For `tenure > 1`:**
  - Mean Ratio: `1.0003` ($\approx 1.00$)
  - Median Ratio: `1.0000`
  - 25th Percentile: `0.9795`
  - 75th Percentile: `1.0196`
  - Standard Deviation: `0.051`
- **Assessment:** Minor deviations ($\pm 2\%$) reflect standard telecom operations: mid-contract package alterations, rate indexation, promotional credits, and usage-based call surcharges. There are no corrupted records.

---

## 6. Outlier & Statistical Distribution Analysis

Statistical outlier detection was executed across all continuous variables using both the **Interquartile Range (IQR) Rule** ($1.5 \times \text{IQR}$) and **Z-Score Standardization** ($|Z| > 3$):

### 6.1 Parametric & Non-Parametric Distribution Summary
| Metric | `tenure` (Months) | `MonthlyCharges` ($) | `TotalCharges` ($) [Valid 7,032] |
| :--- | :--- | :--- | :--- |
| **Count** | 7,043 | 7,043 | 7,032 |
| **Mean** | 32.37 | $64.76 | $2,283.30 |
| **Standard Deviation** | 24.56 | $30.09 | $2,266.77 |
| **Minimum** | 0 | $18.25 | $18.80 |
| **25th Percentile (Q1)**| 9.00 | $35.50 | $401.45 |
| **Median (Q2)** | 29.00 | $70.35 | $1,397.48 |
| **75th Percentile (Q3)**| 55.00 | $89.85 | $3,794.74 |
| **Maximum** | 72 | $118.75 | $8,684.80 |
| **Interquartile Range (IQR)**| 46.00 | $54.35 | $3,393.29 |
| **Skewness** | `+0.2395` (Near Normal) | `-0.2205` (Bimodal) | `+0.9616` (Right-Skewed) |
| **IQR Lower / Upper Fences**| `[-60.0, 124.0]` | `[-46.02, 171.38]` | `[-4688.48, 8884.67]` |
| **IQR Outliers Count** | **0** | **0** | **0** |
| **Z-Score Outliers Count (|Z| > 3)**| **0** | **0** | **0** |

### 6.2 Key Distribution Findings:
1. **Tenure Bimodality:** Tenure exhibits a classic U-shaped distribution common in subscription businesses: a massive cluster of new subscribers (0–6 months) and a dedicated cluster of long-standing loyalists (65–72 months; max tenure capped at 72 months / 6 years).
2. **Monthly Charges Clusters:** Monthly charges display distinct pricing tiers: basic voice-only customers cluster around ~$20/mo, DSL customers around ~$45–$60/mo, and bundled Fiber Optic + Premium streaming packages cluster around ~$85–$115/mo.
3. **Absence of Corrupted Outliers:** Zero negative numbers, zero infinite values, and zero data entry fat-finger typos (e.g., $10,000 monthly fee). All financial distributions align with realistic telco retail pricing models.

---

## 7. Target Variable Analysis: `Churn`

The target column `Churn` captures whether an active customer terminated their telecom contract within the past observation period.

### 7.1 Class Balance & Baseline Metric
- **Retained (`No`):** 5,174 subscribers (**73.46%**)
- **Churned (`Yes`):** 1,869 subscribers (**26.54%**)
- **Class Imbalance Ratio:** ~2.77:1. While not severely imbalanced like credit card fraud, this 26.54% base rate must be accounted for in Power BI KPI cards and downstream predictive retention algorithms.

```
+-----------------------------------------------------------------------+
|  Total Customer Base: 7,043 Subscribers                               |
|  [========================================] 73.46% Retained (5,174)   |
|  [==============                          ] 26.54% Churned  (1,869)   |
+-----------------------------------------------------------------------+
```

### 7.2 Financial Impact of Churn
- **Total Portfolio Monthly Recurring Revenue (MRR):** **$456,116.60**
  - Retained MRR: **$316,985.75** (69.50%)
  - **Churned / Lost MRR:** **$139,130.85 (30.50%)**
  - *Analytical Insight:* Churned subscribers account for **30.50%** of monthly revenue despite being only 26.54% of the customer base. This confirms that **churn disproportionately impacts higher-paying accounts**.
- **Total Historical Portfolio Revenue:** **$16,056,168.70**
  - Retained Lifetime Revenue: $13,193,241.80 (82.17%)
  - Churned Historical Revenue: $2,862,926.90 (17.83%)

### 7.3 Churn Cross-Tabulations & High-Risk Segments

#### A. Contract Term (Primary Churn Driver)
| Contract Type | Total Customers | Retained (`No`) | Churned (`Yes`) | Churn Rate (%) | Churn Contribution (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Month-to-month** | 3,875 | 2,220 | **1,655** | **42.71%** | **88.55%** of all churn |
| **One year** | 1,473 | 1,307 | 166 | 11.27% | 8.88% of all churn |
| **Two year** | 1,695 | 1,647 | 48 | **2.83%** | 2.57% of all churn |

> **Analyst Takeaway:** Month-to-month subscribers are **15.1x more likely to churn** than Two-year contract holders. 88.5% of all churn events originate from month-to-month contracts.

#### B. Tenure Cohorts (The First-Year Drop-Off)
| Tenure Bucket | Total Customers | Retained (`No`) | Churned (`Yes`) | Segment Churn Rate (%) |
| :--- | :---: | :---: | :---: | :---: |
| **0 – 12 Months** | 2,186 | 1,149 | **1,037** | **47.44%** |
| **13 – 24 Months** | 1,024 | 730 | 294 | 28.71% |
| **25 – 36 Months** | 832 | 652 | 180 | 21.63% |
| **37 – 48 Months** | 762 | 617 | 145 | 19.03% |
| **49 – 60 Months** | 832 | 712 | 120 | 14.42% |
| **61 – 72 Months** | 1,407 | 1,314 | 93 | **6.61%** |

> **Analyst Takeaway:** Over **55.48% (1,037 / 1,869)** of all churn occurs during the first year of tenure. Once a customer reaches year 5 (49+ months), churn plummets below 10%.

#### C. Internet Service & Technology
| Technology | Total Customers | Retained (`No`) | Churned (`Yes`) | Churn Rate (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Fiber optic** | 3,096 | 1,799 | **1,297** | **41.89%** |
| **DSL** | 2,421 | 1,962 | 459 | 18.96% |
| **No Internet** | 1,526 | 1,413 | 113 | 7.40% |

> **Analyst Takeaway:** Fiber Optic subscribers exhibit a very high 41.89% churn rate, compared to 18.96% for DSL. This suggests either competitive pricing pressure, network quality issues, or bill shock among Fiber customers.

#### D. Payment Method (Friction Factor)
| Payment Method | Total Customers | Retained (`No`) | Churned (`Yes`) | Churn Rate (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Electronic check** | 2,365 | 1,294 | **1,071** | **45.29%** |
| **Mailed check** | 1,612 | 1,304 | 308 | 19.11% |
| **Bank transfer (auto)**| 1,544 | 1,286 | 258 | 16.71% |
| **Credit card (auto)** | 1,522 | 1,290 | 232 | **15.24%** |

> **Analyst Takeaway:** Electronic check payments suffer nearly triple the churn rate of automated credit card or bank drafts (45.29% vs ~15.5%).

#### E. Service Protection & Support Services
| Service Feature | Without Service Churn Rate | With Service Churn Rate | Retention Uplift |
| :--- | :---: | :---: | :---: |
| **TechSupport** | **41.64%** (No Support) | **15.17%** (Has Support) | **+26.47% points** |
| **OnlineSecurity**| **41.77%** (No Security) | **14.61%** (Has Security) | **+27.16% points** |
| **OnlineBackup** | **39.93%** (No Backup) | **21.53%** (Has Backup) | **+18.40% points** |

---

## 8. Data Cleaning & Transformation Blueprint (Phase 2 Roadmap)

To prepare this dataset for downstream processing across Python, MySQL, Excel, and Power BI without modifying the raw source file, the following transformation rules are recommended for Phase 2:

### 8.1 Resolution of the 11 `TotalCharges` Missing Values
* **Root Cause:** 11 customers with `tenure = 0` who have not completed their first billing cycle.
* **Recommended Action:** **Impute `TotalCharges = 0.00`** for records where `tenure == 0`.
  - *Why not delete?* Deleting removes 11 high-value, newly onboarded subscribers on multi-year contracts ($0.156\%$ data loss, but distorts cohort inflow tracking).
  - *Why not mean/median?* Imputing $2,283 (mean) onto a customer with 0 months of tenure violates basic accounting logic and corrupts financial calculations.
  - *Why not `MonthlyCharges`?* Although they signed up for that monthly amount, no completed bill has been posted yet. $0.00 is the only logically coherent historical total charge.

### 8.2 Data Type Casting & Schema Specifications
| Platform | Target Field | Source Type | Cleaned Type | Expression / Specification |
| :--- | :--- | :--- | :--- | :--- |
| **Python (Pandas)** | `TotalCharges` | `object` | `float64` | `df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].str.strip()).fillna(0.0)` |
| **Python (Pandas)** | `SeniorCitizen` | `int64` | `category` / `object`| `df['SeniorCitizen_Label'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})` |
| **MySQL** | `customerID` | `VARCHAR(255)` | `VARCHAR(10)` | `customerID VARCHAR(10) PRIMARY KEY` |
| **MySQL** | `TotalCharges` | `VARCHAR` | `DECIMAL(10,2)`| `TotalCharges DECIMAL(10,2) NOT NULL DEFAULT 0.00` |
| **MySQL** | `MonthlyCharges`| `DOUBLE` | `DECIMAL(10,2)`| `MonthlyCharges DECIMAL(10,2) NOT NULL` |
| **Power BI / DAX** | `TotalCharges` | `Text` | `Fixed Decimal ($)` | Transform via Power Query: Replace `" "` with `"0"`, set type to `Currency` |
| **Power BI / DAX** | `tenure_group` | *New Column* | `Text` | Grouping into `0-12m`, `13-24m`, `25-36m`, `37-48m`, `49-60m`, `61-72m` |

### 8.3 Recommended Feature Engineering for Analytics & Dashboards
1. **Tenure Cohorts:** Group tenure into 6 clean annual buckets (`0-12m`, `13-24m`, `25-36m`, `37-48m`, `49-60m`, `61-72m`) for Power BI cohort curves.
2. **Payment Channel Category:** Group into `Automatic` (`Bank transfer`, `Credit card`) vs `Manual` (`Electronic check`, `Mailed check`).
3. **Product Bundling Score:** Compute an integer count `Total_Services_Subscribed` (0 to 8) tracking how many ancillary services (Streaming, Security, Tech Support, etc.) a customer holds.
4. **Monthly Charges Tier:** Segment `MonthlyCharges` into `<$35` (Basic), `$35–$70` (Standard), `$70–$95` (Premium), `>$95` (Ultra/High ARPU).

---

## 9. Phase 1 Sign-Off & Next Steps

### Summary of Audit Status
- [x] Read CSV dataset without modifying source.
- [x] Identified 7,043 rows and 21 columns.
- [x] Documented all 21 columns in an enterprise data dictionary.
- [x] Isolated 11 whitespace missing values in `TotalCharges`.
- [x] Confirmed zero duplicate customer IDs.
- [x] Documented data type conversion requirements.
- [x] Validated semantic cross-service coherence (Phone, Internet, Add-ons).
- [x] Audited `TotalCharges` vs `tenure` mathematical correlation.
- [x] Completed IQR & Z-score outlier investigations.
- [x] Conducted exhaustive target variable (`Churn`) risk and revenue analysis.
- [x] Created Phase 1 Data Understanding & Quality Report in `documentation/`.

### Ready for Phase 2: Data Cleaning & Preprocessing
Upon your review and explicit approval, we will proceed to Phase 2:
1. Implement reproducible cleaning script in Python (`python/data_cleaning.py`).
2. Export clean dataset (`dataset/cleaned_telco_customer_churn.csv`).
3. Prepare MySQL table DDL and loading scripts (`sql/schema_setup.sql`).
4. Prepare clean data model for Excel and Power BI import.

---
*Report generated and archived at `documentation/DATA_UNDERSTANDING_AND_QUALITY_REPORT.md`.*
