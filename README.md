# Customer Churn & Retention Intelligence System

An end-to-end Data Analytics and Machine Learning project that analyzes telecom customer behavior, identifies churn patterns, evaluates revenue impact, and predicts customers who are likely to leave.

## Project Overview

Customer churn is a major challenge for subscription-based businesses. Losing customers directly affects recurring revenue and long-term business growth.

This project uses the IBM Telco Customer Churn dataset to analyze customer behavior, identify churn drivers, evaluate revenue at risk, and build machine learning models to predict customer churn.

The project combines Excel, Python, SQL, Power BI, and Machine Learning into a complete analytics workflow.

## Business Objectives

- Understand overall customer churn patterns.
- Identify customer segments with high churn rates.
- Analyze revenue loss caused by customer churn.
- Identify customers who may be at risk of leaving.
- Build machine learning models to predict customer churn.
- Generate insights that can support customer retention strategies.

## Technology Stack

| Category | Tools |
|---|---|
| Data Cleaning | Excel, Python |
| Data Analysis | Python, Pandas, NumPy |
| Database | MySQL |
| Query Language | SQL |
| Data Visualization | Power BI |
| Machine Learning | Scikit-learn |
| Models | Logistic Regression, Random Forest |
| Version Control | Git, GitHub |

## Dataset

**Source:** IBM Telco Customer Churn Dataset

- Total Records: 7,043 customers
- Total Columns: 25
- Target Variable: Churn
- Churned Customers: 1,869
- Retained Customers: 5,174

## Project Workflow

1. Data Collection – Load the telecom customer dataset.
2. Data Cleaning – Handle missing values, correct data types, and prepare the dataset.
3. Exploratory Data Analysis – Analyze churn patterns and customer characteristics.
4. SQL Analysis – Perform business queries using aggregation, joins, CTEs, and window functions.
5. Machine Learning – Train and evaluate churn prediction models.
6. Power BI – Build dashboards to communicate business insights.
7. Business Recommendations – Identify customer segments that need retention attention.

## Key Business Insights

- Overall customer churn rate: 26.54%.
- Monthly revenue: $456,116.60.
- Revenue associated with churned customers: $139,130.85.
- Customers with shorter tenure and month-to-month contracts show important churn patterns.

*Revenue figures are based on the analyzed dataset and its monthly charge values.*

## Machine Learning

Two classification models were evaluated:

- Logistic Regression
- Random Forest

### Model Evaluation Results

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| ROC-AUC | 0.8429 | 0.8345 |
| PR-AUC | 0.6443 | 0.6301 |
| Accuracy | 74.10% | 77.43% |
| Precision | 50.76% | 56.86% |
| Recall | 79.95% | 62.03% |
| F1 Score | 0.6210 | 0.5934 |

**Selected Model:** Logistic Regression based on ROC-AUC.

The model generates churn probabilities for customers to help identify customers who may need retention attention.

Note: These are model evaluation results from a held-out test dataset. Predicted probabilities are estimates and should not be interpreted as guaranteed outcomes.

## Power BI Dashboard

The existing Power BI report contains three analytical pages:

1. **Executive Overview** – Overall business KPIs and churn performance.
2. **Customer Churn Analysis** – Customer demographics, services, and churn patterns.
3. **Revenue & Retention Intelligence** – Revenue impact and rule-based customer risk analysis.

A fourth page, **Predictive Churn Intelligence**, is planned for the machine learning prediction integration.

## Rule-Based Risk Analysis

A separate heuristic risk score is used to identify customers who may require attention.

Risk factors include:

- Month-to-month contract
- Fiber optic internet service
- Electronic check payment method
- Customer tenure of 12 months or less

Customers with a score of 7 or above are classified as Critical Risk.

This is a business rule-based approach, not a machine learning prediction.

## Project Structure

```text
Customer-Churn-Retention-Intelligence/
│
├── dataset/
├── excel/
├── python/
├── sql/
├── powerbi/
├── documentation/
├── src/
├── models/
├── outputs/
│   └── ml/
│
├── README.md
├── requirements.txt
└── .gitignore
```

*Some generated files and subfolders may vary depending on the project version.*

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/hareeshvavilapalli/Customer-Churn-Retention-Intelligence.git
```

### 2. Navigate to the Project

```bash
cd Customer-Churn-Retention-Intelligence
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Machine Learning Script

```bash
python src/churn_prediction.py
```

Check the project documentation for the exact dataset path and Power BI integration instructions.

## Future Improvements

- Complete the Predictive Churn Intelligence Power BI page.
- Integrate automated churn prediction into a business reporting workflow.
- Develop customer-specific retention recommendations.
- Explore model calibration and threshold optimization.
- Deploy the prediction model through a web application.

## Learning Outcomes

Through this project, I worked on:

- Data cleaning and preprocessing.
- Exploratory data analysis.
- SQL-based business analysis.
- Dashboard development.
- Classification model training and evaluation.
- Business-oriented interpretation of analytical results.

## Author

**Hareesh Vavilapalli**

GitHub: [hareeshvavilapalli](https://github.com/hareeshvavilapalli)

---

*This project was developed as a portfolio project to demonstrate practical skills in Data Analytics, SQL, Power BI, and Machine Learning.*
