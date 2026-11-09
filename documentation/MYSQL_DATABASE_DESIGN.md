# MYSQL DATABASE ARCHITECTURE & SCHEMA DESIGN
**Project:** Customer Churn & Retention Intelligence System  
**Database Name:** `customer_churn_db`  
**Target RDBMS:** MySQL 8.0+ (InnoDB Engine, UTF-8 Unicode Encoding)  
**Author:** Senior Data Analyst  
**Date:** November 8, 2026  
**Status:** Architecture Designed, Scripted, and Validated  

---

## 1. Design Overview & Philosophy

The database architecture for the **Customer Churn & Retention Intelligence System** is engineered to fulfill two complementary enterprise objectives:
1. **High-Performance Analytical Querying (OLAP Consolidation):** A master table `customers` preserving all 25 cleaned attributes and engineered features, heavily indexed on primary query dimensions (Contract, Churn, InternetService, PaymentMethod, tenure_group).
2. **Relational Normalization & Referential Integrity (Star Schema Architecture):** A normalized dimensional model partitioning attributes into three dimension tables (`dim_demographics`, `dim_services`, `dim_contracts`) and one fact table (`fact_billing_churn`), linked via strict foreign key constraints.

---

## 2. Entity-Relationship Architecture (Star Schema)

```mermaid
erDiagram
    customers ||--|| dim_demographics : "identifies (1:1)"
    customers ||--|| dim_services : "subscribes (1:1)"
    customers ||--|| dim_contracts : "binds (1:1)"
    customers ||--|| fact_billing_churn : "bills (1:1)"

    customers {
        varchar(10) customerID PK
        varchar(6) gender
        tinyint SeniorCitizen
        varchar(3) Partner
        varchar(3) Dependents
        smallint tenure
        varchar(3) PhoneService
        varchar(16) MultipleLines
        varchar(11) InternetService
        varchar(19) OnlineSecurity
        varchar(19) OnlineBackup
        varchar(19) DeviceProtection
        varchar(19) TechSupport
        varchar(19) StreamingTV
        varchar(19) StreamingMovies
        varchar(14) Contract
        varchar(3) PaperlessBilling
        varchar(25) PaymentMethod
        decimal(10,2) MonthlyCharges
        decimal(10,2) TotalCharges
        varchar(3) Churn
        varchar(3) SeniorCitizen_Label
        varchar(10) tenure_group
        varchar(10) payment_category
        tinyint service_count
    }

    dim_demographics {
        varchar(10) customerID PK,FK
        varchar(6) gender
        tinyint SeniorCitizen
        varchar(3) SeniorCitizen_Label
        varchar(3) Partner
        varchar(3) Dependents
    }

    dim_services {
        varchar(10) customerID PK,FK
        varchar(3) PhoneService
        varchar(16) MultipleLines
        varchar(11) InternetService
        varchar(19) OnlineSecurity
        varchar(19) OnlineBackup
        varchar(19) DeviceProtection
        varchar(19) TechSupport
        varchar(19) StreamingTV
        varchar(19) StreamingMovies
        tinyint service_count
    }

    dim_contracts {
        varchar(10) customerID PK,FK
        varchar(14) Contract
        varchar(3) PaperlessBilling
        varchar(25) PaymentMethod
        varchar(10) payment_category
        smallint tenure
        varchar(10) tenure_group
    }

    fact_billing_churn {
        varchar(10) customerID PK,FK
        decimal(10,2) MonthlyCharges
        decimal(10,2) TotalCharges
        varchar(3) Churn
    }
```

---

## 3. Comprehensive Table Schema & Data Types

### 3.1 Master Table: `customers`
The core transactional and analytical repository containing all 7,043 customer accounts:

| Column Name | MySQL Data Type | Nullable | Key / Constraints | Business Description & Validation Rule |
| :--- | :--- | :---: | :--- | :--- |
| `customerID` | `VARCHAR(10)` | NO | **PRIMARY KEY** | Unique customer alphanumeric code (format: `0000-AAAAA`). |
| `gender` | `VARCHAR(6)` | NO | `CHECK IN ('Male', 'Female')` | Subscriber gender. |
| `SeniorCitizen` | `TINYINT` | NO | `CHECK IN (0, 1)` | Binary indicator (0 = Non-Senior, 1 = Senior Citizen). |
| `Partner` | `VARCHAR(3)` | NO | `CHECK IN ('Yes', 'No')` | Marital or domestic partner status. |
| `Dependents` | `VARCHAR(3)` | NO | `CHECK IN ('Yes', 'No')` | Presence of dependent family members in household. |
| `tenure` | `SMALLINT` | NO | `CHECK (tenure >= 0)` | Customer subscription duration in completed months (0 to 72). |
| `PhoneService` | `VARCHAR(3)` | NO | `CHECK IN ('Yes', 'No')` | Core voice subscription status. |
| `MultipleLines` | `VARCHAR(16)` | NO | Categorical | Multi-line telephone service (`Yes`, `No`, `No phone service`). |
| `InternetService` | `VARCHAR(11)` | NO | Indexed | Broadband connection technology (`DSL`, `Fiber optic`, `No`). |
| `OnlineSecurity` | `VARCHAR(19)` | NO | Categorical | Cybersecurity add-on plan (`Yes`, `No`, `No internet service`). |
| `OnlineBackup` | `VARCHAR(19)` | NO | Categorical | Cloud backup service (`Yes`, `No`, `No internet service`). |
| `DeviceProtection`| `VARCHAR(19)` | NO | Categorical | Hardware damage insurance (`Yes`, `No`, `No internet service`). |
| `TechSupport` | `VARCHAR(19)` | NO | Categorical | Priority troubleshooting (`Yes`, `No`, `No internet service`). |
| `StreamingTV` | `VARCHAR(19)` | NO | Categorical | IPTV television streaming package (`Yes`, `No`, `No internet service`). |
| `StreamingMovies`| `VARCHAR(19)` | NO | Categorical | Movie streaming service (`Yes`, `No`, `No internet service`). |
| `Contract` | `VARCHAR(14)` | NO | Indexed | Contract term (`Month-to-month`, `One year`, `Two year`). |
| `PaperlessBilling`| `VARCHAR(3)` | NO | Categorical | Digital billing opt-in preference (`Yes`, `No`). |
| `PaymentMethod` | `VARCHAR(25)` | NO | Indexed | Invoicing settlement channel (`Electronic check`, `Mailed check`, etc.). |
| `MonthlyCharges`| `DECIMAL(10,2)`| NO | `CHECK >= 0.00` | Recurring monthly fee ($18.25 to $118.75). |
| `TotalCharges` | `DECIMAL(10,2)`| NO | `CHECK >= 0.00` | Cumulative lifetime charges ($0.00 to $8,684.80). |
| `Churn` | `VARCHAR(3)` | NO | Indexed | Primary target variable (`Yes`, `No`). |
| `SeniorCitizen_Label`| `VARCHAR(3)`| NO | Categorical | User-friendly label for dashboards (`'Yes'`/`'No'`). |
| `tenure_group` | `VARCHAR(10)` | NO | Indexed | Lifecycle cohort (`0-12m`, `13-24m`, `25-36m`, `37-48m`, `49-60m`, `61-72m`). |
| `payment_category`| `VARCHAR(10)` | NO | Indexed | Operational friction category (`Automatic` vs `Manual`). |
| `service_count` | `TINYINT` | NO | `CHECK (1 TO 9)` | Total count of subscribed services across voice, data, and add-ons. |

---

## 4. Indexing Strategy & Performance Optimization

To deliver millisecond query responses on filtering, joining, and aggregation operations across 7,043 rows, the following indexes are deployed:

| Index Name | Target Column(s) | Index Type | Query Optimization Rationale |
| :--- | :--- | :--- | :--- |
| `PRIMARY` | `customerID` | B-Tree Clustered | Guarantees instant O(1) single-customer lookups and primary key integrity. |
| `idx_customers_churn` | `Churn` | B-Tree Secondary | Accelerates binary churn cohort filtering (`WHERE Churn = 'Yes'`). |
| `idx_customers_contract` | `Contract` | B-Tree Secondary | Optimizes multi-contract aggregations (`GROUP BY Contract`). |
| `idx_customers_internet` | `InternetService` | B-Tree Secondary | Enhances broadband technology segment queries (`GROUP BY InternetService`). |
| `idx_customers_payment` | `PaymentMethod` | B-Tree Secondary | Speeds up settlement method churn cross-tabulations. |
| `idx_customers_tenure_grp`| `tenure_group` | B-Tree Secondary | Accelerates lifecycle retention curve groupings. |
| `idx_customers_pay_cat` | `payment_category` | B-Tree Secondary | Optimizes automated vs manual payment comparisons. |
| `idx_customers_contract_churn`| `Contract`, `Churn` | Composite B-Tree | Maximizes performance for joint contract and churn cross-filtering. |
| `idx_customers_monthly_charges`| `MonthlyCharges` | B-Tree Secondary | Optimizes numerical range filtering (e.g. top quartile high-ARPU accounts). |

---

## 5. Storage Engine & Environmental Configuration

- **Storage Engine:** `InnoDB`
  - ACID transaction compliance.
  - Foreign key referential integrity constraints with `ON DELETE CASCADE`.
  - Row-level locking for concurrent analytical operations.
- **Character Set & Collation:** `utf8mb4` with `utf8mb4_unicode_ci`
  - Universal multilingual compatibility.
  - Case-insensitive string comparisons preventing subtle casing discrepancies.
- **SQL Mode Recommendations:** `STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION`
  - Rejects truncated or invalid data inputs automatically during ingestion.

---

## 6. Execution & Deployment Artifacts

The database architecture is fully codified in the following scripts:
1. [`sql/01_create_database.sql`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/sql/01_create_database.sql) — Database creation and character set setup.
2. [`sql/02_create_tables.sql`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/sql/02_create_tables.sql) — DDL script defining tables, primary keys, check constraints, and secondary indexes.
3. [`sql/03_load_data.sql`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/sql/03_load_data.sql) — High-speed bulk CSV loading using `LOAD DATA INFILE`.
4. [`python/load_to_mysql.py`](file:///c:/Users/V.Leela%20prasad/OneDrive/Desktop/Customer-Churn-Retention-Intelligence/python/load_to_mysql.py) — Automated Python database loader utilizing parameterized batch inserts.

---
*Document archived at `documentation/MYSQL_DATABASE_DESIGN.md`.*
