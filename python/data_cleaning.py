"""
Customer Churn & Retention Intelligence System
Module: Data Cleaning & Transformation Pipeline
Phase: Phase 2 (Enterprise ETL & Feature Engineering)
Author: Senior Data Analyst
Tech Stack: Python, Pandas, OpenPyXL, MySQL, Power BI

This module provides an automated, reproducible, and non-destructive pipeline
to ingest raw Telco customer churn data, perform audit checks, handle anomalies
(such as zero-tenure blank TotalCharges), engineer strategic analytical features,
validate data integrity against raw baselines, and export cleaned artifacts.
"""

import os
import sys
import logging
import argparse
import numpy as np
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("TelcoChurnETL")


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Ingest raw customer churn CSV dataset without altering the original file.
    
    Args:
        filepath (str): Path to raw CSV file.
        
    Returns:
        pd.DataFrame: Raw dataframe.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Source file not found at: {filepath}")
    logger.info(f"Loading raw dataset from: {filepath}")
    df = pd.read_csv(filepath)
    logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
    return df


def audit_raw_data(df: pd.DataFrame) -> dict:
    """
    Run baseline diagnostic audit on the raw dataset.
    
    Args:
        df (pd.DataFrame): Raw dataframe.
        
    Returns:
        dict: Diagnostic metrics summary.
    """
    total_rows, total_cols = df.shape
    dup_ids = df['customerID'].duplicated().sum()
    dup_rows = df.duplicated().sum()
    native_nulls = df.isna().sum().to_dict()
    
    # Check blank strings in TotalCharges
    tc_blanks = (df['TotalCharges'].astype(str).str.strip() == '').sum()
    tenure_zeros = (df['tenure'] == 0).sum()
    
    audit_results = {
        "total_rows": total_rows,
        "total_cols": total_cols,
        "duplicate_customer_ids": int(dup_ids),
        "duplicate_rows": int(dup_rows),
        "native_null_count": sum(native_nulls.values()),
        "totalcharges_blank_count": int(tc_blanks),
        "tenure_zero_count": int(tenure_zeros),
        "churn_distribution": df['Churn'].value_counts().to_dict(),
    }
    logger.info(f"Raw Audit Results: {audit_results}")
    return audit_results


def clean_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw Telco customer churn dataset:
    - Creates a defensive deep copy (preserves raw).
    - Trims leading/trailing whitespace across all text columns.
    - Resolves 11 zero-tenure blank TotalCharges records by imputing 0.00.
    - Casts TotalCharges to float64.
    - Validates data types and primary key format.
    
    Args:
        df_raw (pd.DataFrame): Raw dataframe.
        
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    logger.info("Initiating non-destructive data cleaning...")
    df = df_raw.copy(deep=True)
    
    # 1. Strip whitespace from all string/object columns
    object_cols = df.select_dtypes(include='object').columns
    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()
        
    # 2. Investigate and clean TotalCharges
    # Identify records where TotalCharges is blank or empty
    blank_mask = df['TotalCharges'] == ''
    logger.info(f"Detected {blank_mask.sum()} blank TotalCharges records.")
    
    # Verify that ALL blank TotalCharges strictly correspond to tenure == 0
    tenure_zero_mask = df['tenure'] == 0
    if not (blank_mask == tenure_zero_mask).all():
        mismatch_count = (blank_mask != tenure_zero_mask).sum()
        raise ValueError(f"Integrity Error: {mismatch_count} blank TotalCharges records do not match tenure == 0!")
        
    logger.info("Integrity check passed: All 11 blank TotalCharges records strictly belong to tenure == 0 customers.")
    
    # Impute 0.0 for tenure == 0 records and convert column to numeric float64
    df.loc[tenure_zero_mask, 'TotalCharges'] = '0.0'
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='raise')
    logger.info("Successfully cast TotalCharges to float64 with $0.00 imputed for zero-tenure accounts.")
    
    # 3. Ensure MonthlyCharges is float64 and tenure is int64
    df['MonthlyCharges'] = df['MonthlyCharges'].astype(float)
    df['tenure'] = df['tenure'].astype(int)
    
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer business-critical features for retention intelligence and BI dashboards:
    1. SeniorCitizen_Label: Categorical 'Yes'/'No' for consistent dashboard presentation.
    2. tenure_group: 6 annual cohorts ('0-12m', '13-24m', '25-36m', '37-48m', '49-60m', '61-72m').
    3. payment_category: 'Automatic' vs 'Manual' based on PaymentMethod.
    4. service_count: Total count of active subscribed core & value-added services (range 1-9).
    
    Args:
        df (pd.DataFrame): Cleaned dataframe.
        
    Returns:
        pd.DataFrame: Dataframe with engineered features.
    """
    logger.info("Engineering business features...")
    df_feat = df.copy()
    
    # 1. SeniorCitizen_Label
    df_feat['SeniorCitizen_Label'] = df_feat['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
    
    # 2. Tenure Cohort Groups
    bins = [-1, 12, 24, 36, 48, 60, 72]
    labels = ['0-12m', '13-24m', '25-36m', '37-48m', '49-60m', '61-72m']
    df_feat['tenure_group'] = pd.cut(df_feat['tenure'], bins=bins, labels=labels)
    
    # 3. Payment Category (Automatic vs Manual)
    df_feat['payment_category'] = df_feat['PaymentMethod'].apply(
        lambda x: 'Automatic' if 'automatic' in x.lower() else 'Manual'
    )
    
    # 4. Service Count (1 to 9)
    # Binary services where 'Yes' indicates subscription
    binary_services = [
        'PhoneService', 'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]
    service_matrix = (df_feat[binary_services] == 'Yes').astype(int)
    
    # InternetService counts as 1 if customer has DSL or Fiber optic
    has_internet = df_feat['InternetService'].isin(['DSL', 'Fiber optic']).astype(int)
    
    df_feat['service_count'] = service_matrix.sum(axis=1) + has_internet
    logger.info(f"Engineered 4 new features. New dataset shape: {df_feat.shape}")
    return df_feat


def validate_cleaned_dataset(df_raw: pd.DataFrame, df_cleaned: pd.DataFrame) -> bool:
    """
    Rigorous cross-validation between raw and cleaned datasets.
    
    Args:
        df_raw (pd.DataFrame): Raw dataframe.
        df_cleaned (pd.DataFrame): Cleaned & enriched dataframe.
        
    Returns:
        bool: True if all validation assertions pass.
    """
    logger.info("Running rigorous validation checks...")
    
    # 1. Row count validation
    assert len(df_cleaned) == 7043, f"Expected 7043 rows, found {len(df_cleaned)}"
    assert len(df_cleaned) == len(df_raw), "Row count mismatch between raw and cleaned datasets!"
    
    # 2. Column count validation (21 original + 4 engineered = 25)
    assert len(df_cleaned.columns) == 25, f"Expected 25 columns, found {len(df_cleaned.columns)}"
    
    # 3. Primary Key Uniqueness
    assert df_cleaned['customerID'].nunique() == 7043, "CustomerID is not 100% unique!"
    assert df_cleaned['customerID'].duplicated().sum() == 0, "Duplicate customer IDs detected!"
    
    # 4. Zero Missing Values
    null_counts = df_cleaned.isna().sum().sum()
    assert null_counts == 0, f"Detected {null_counts} null values in cleaned dataset!"
    
    # 5. Zero-tenure records validation
    t0_records = df_cleaned[df_cleaned['tenure'] == 0]
    assert len(t0_records) == 11, f"Expected exactly 11 zero-tenure records, found {len(t0_records)}"
    assert (t0_records['TotalCharges'] == 0.0).all(), "Zero-tenure TotalCharges not strictly 0.00!"
    
    # 6. Target Variable Integrity
    raw_churn = df_raw['Churn'].str.strip().value_counts().to_dict()
    clean_churn = df_cleaned['Churn'].value_counts().to_dict()
    assert raw_churn == clean_churn, f"Churn distribution changed! Raw: {raw_churn}, Cleaned: {clean_churn}"
    
    # 7. Financial Consistency
    raw_mrr = df_raw['MonthlyCharges'].sum()
    clean_mrr = df_cleaned['MonthlyCharges'].sum()
    assert np.isclose(raw_mrr, clean_mrr, atol=1e-4), "MonthlyCharges sum mismatch!"
    
    # Valid raw TotalCharges sum (excluding the 11 blank records)
    valid_raw_tc = pd.to_numeric(df_raw['TotalCharges'].astype(str).str.strip(), errors='coerce').sum()
    clean_tc = df_cleaned['TotalCharges'].sum()
    assert np.isclose(valid_raw_tc, clean_tc, atol=1e-4), "TotalCharges sum mismatch against valid raw baseline!"
    
    logger.info("ALL VALIDATION CHECKS PASSED PERFECTLY!")
    logger.info(f"- Total Rows: {len(df_cleaned):,}")
    logger.info(f"- Unique Customers: {df_cleaned['customerID'].nunique():,}")
    logger.info(f"- Zero-Tenure TotalCharges ($0.00): {len(t0_records)}")
    logger.info(f"- Monthly Recurring Revenue (MRR): ${clean_mrr:,.2f}")
    logger.info(f"- Total Cumulative Revenue: ${clean_tc:,.2f}")
    logger.info(f"- Churn Distribution: Retained={clean_churn['No']:,} ({clean_churn['No']/len(df_cleaned):.2%}), "
                f"Churned={clean_churn['Yes']:,} ({clean_churn['Yes']/len(df_cleaned):.2%})")
    return True


def save_cleaned_data(df: pd.DataFrame, csv_output_path: str) -> None:
    """
    Export cleaned dataset to CSV.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe.
        csv_output_path (str): File destination path for CSV.
    """
    os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)
    df.to_csv(csv_output_path, index=False)
    logger.info(f"Cleaned dataset saved successfully to: {csv_output_path}")


def main():
    """
    Execute end-to-end cleaning and feature engineering pipeline.
    """
    parser = argparse.ArgumentParser(description="Clean and enrich IBM Telco Customer Churn dataset.")
    parser.add_argument("--input", default="dataset/WA_Fn-UseC_-Telco-Customer-Churn.csv", help="Input raw CSV path")
    parser.add_argument("--output_csv", default="dataset/cleaned_telco_customer_churn.csv", help="Output cleaned CSV path")
    args = parser.parse_args()
    
    logger.info("=== STARTING PHASE 2: DATA CLEANING PIPELINE ===")
    df_raw = load_raw_data(args.input)
    audit_raw_data(df_raw)
    df_cleaned = clean_data(df_raw)
    df_enriched = engineer_features(df_cleaned)
    validate_cleaned_dataset(df_raw, df_enriched)
    save_cleaned_data(df_enriched, args.output_csv)
    logger.info("=== PHASE 2 PIPELINE EXECUTED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
