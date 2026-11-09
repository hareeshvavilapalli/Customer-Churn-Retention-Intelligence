"""
Customer Churn & Retention Intelligence System
Script: python/load_to_mysql.py
Description: Automated Python ETL loader to ingest cleaned CSV into MySQL database.
Author: Senior Data Analyst

Features:
- Configurable connection parameters (host, port, user, password, database).
- Executes database and table DDL creation.
- Executes batch parameterized INSERTs (bypassing LOAD DATA LOCAL INFILE permissions).
- Loads both the consolidated `customers` table and normalized star-schema tables.
- Runs post-load validation assertions.
"""

import os
import sys
import argparse
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("MySQLLoader")


def get_mysql_connection(host, port, user, password, database=None):
    """
    Establish connection to MySQL using either mysql.connector or pymysql.
    """
    conn = None
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        logger.info("Connected to MySQL using mysql.connector.")
        return conn
    except ImportError:
        pass

    try:
        import pymysql
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset="utf8mb4"
        )
        logger.info("Connected to MySQL using PyMySQL.")
        return conn
    except ImportError:
        pass

    raise ImportError(
        "Neither 'mysql.connector' nor 'pymysql' is installed. "
        "Please install one of them via: pip install mysql-connector-python or pip install pymysql"
    )


def execute_sql_file(conn, sql_filepath):
    """
    Execute multi-statement SQL script file.
    """
    if not os.path.exists(sql_filepath):
        raise FileNotFoundError(f"SQL file not found: {sql_filepath}")
        
    logger.info(f"Executing SQL script: {sql_filepath}")
    with open(sql_filepath, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Split statements by semicolon
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
    cursor = conn.cursor()
    for stmt in statements:
        # Ignore comments or empty statements
        clean_stmt = "\n".join([line for line in stmt.split("\n") if not line.strip().startswith("--")])
        if clean_stmt.strip():
            cursor.execute(clean_stmt)
    conn.commit()
    cursor.close()
    logger.info(f"Successfully executed {len(statements)} statements from {sql_filepath}.")


def load_cleaned_csv_to_mysql(conn, csv_filepath):
    """
    Load cleaned CSV dataset into MySQL `customers` table using batch insert.
    """
    if not os.path.exists(csv_filepath):
        raise FileNotFoundError(f"CSV file not found: {csv_filepath}")
        
    logger.info(f"Reading cleaned CSV from: {csv_filepath}")
    df = pd.read_csv(csv_filepath)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns into memory.")

    # Step 1: Pre-load Data Integrity Checks
    null_count = df.isna().sum().sum()
    if null_count > 0:
        raise ValueError(f"Integrity Error: Found {null_count} unexpected NULL values in CSV!")
        
    dup_ids = df['customerID'].duplicated().sum()
    if dup_ids > 0:
        raise ValueError(f"Integrity Error: Found {dup_ids} duplicate customer IDs in CSV!")

    logger.info("Pre-load checks passed: 0 NULLs, 0 duplicate customer IDs.")

    cursor = conn.cursor()
    
    try:
        # Step 2: Disable FK checks for safe idempotent truncation
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE dim_demographics;")
        cursor.execute("TRUNCATE TABLE dim_services;")
        cursor.execute("TRUNCATE TABLE dim_contracts;")
        cursor.execute("TRUNCATE TABLE fact_billing_churn;")
        cursor.execute("TRUNCATE TABLE customers;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        cols = list(df.columns)
        col_str = ", ".join(cols)
        placeholders = ", ".join(["%s"] * len(cols))
        insert_sql = f"INSERT INTO customers ({col_str}) VALUES ({placeholders});"

        # Format records as native Python types with explicit numeric casting
        records = []
        for row in df.itertuples(index=False):
            row_dict = row._asdict()
            record = (
                str(row_dict['customerID']),
                str(row_dict['gender']),
                int(row_dict['SeniorCitizen']),
                str(row_dict['Partner']),
                str(row_dict['Dependents']),
                int(row_dict['tenure']),
                str(row_dict['PhoneService']),
                str(row_dict['MultipleLines']),
                str(row_dict['InternetService']),
                str(row_dict['OnlineSecurity']),
                str(row_dict['OnlineBackup']),
                str(row_dict['DeviceProtection']),
                str(row_dict['TechSupport']),
                str(row_dict['StreamingTV']),
                str(row_dict['StreamingMovies']),
                str(row_dict['Contract']),
                str(row_dict['PaperlessBilling']),
                str(row_dict['PaymentMethod']),
                round(float(row_dict['MonthlyCharges']), 2),
                round(float(row_dict['TotalCharges']), 2),
                str(row_dict['Churn']),
                str(row_dict['SeniorCitizen_Label']),
                str(row_dict['tenure_group']),
                str(row_dict['payment_category']),
                int(row_dict['service_count'])
            )
            records.append(record)

        logger.info(f"Inserting {len(records)} records into MySQL `customers` table...")
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            cursor.executemany(insert_sql, batch)
            logger.info(f"  Inserted rows {i + 1} to {min(i + batch_size, len(records))}")

        # Step 3: Populate normalized dimensional tables
        logger.info("Populating normalized dimension and fact tables...")
        cursor.execute("INSERT INTO dim_demographics SELECT customerID, gender, SeniorCitizen, SeniorCitizen_Label, Partner, Dependents FROM customers;")
        cursor.execute("INSERT INTO dim_services SELECT customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, service_count FROM customers;")
        cursor.execute("INSERT INTO dim_contracts SELECT customerID, Contract, PaperlessBilling, PaymentMethod, payment_category, tenure, tenure_group FROM customers;")
        cursor.execute("INSERT INTO fact_billing_churn SELECT customerID, MonthlyCharges, TotalCharges, Churn FROM customers;")
        
        # Step 4: Commit entire transaction atomically
        conn.commit()
        logger.info("Transaction committed successfully. All tables populated.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error during loading. Transaction rolled back! Error: {e}")
        raise e
    finally:
        cursor.close()


def run_post_load_validation(conn):
    """
    Verify loaded record counts, sums, and churn distributions.
    """
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM customers;")
    total_records = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT customerID) FROM customers;")
    unique_ids = cursor.fetchone()[0]
    
    cursor.execute("SELECT ROUND(SUM(MonthlyCharges), 2), ROUND(SUM(TotalCharges), 2) FROM customers;")
    mrr_sum, tc_sum = cursor.fetchone()
    
    cursor.execute("SELECT Churn, COUNT(*) FROM customers GROUP BY Churn;")
    churn_counts = dict(cursor.fetchall())
    
    cursor.close()
    
    logger.info("=== POST-LOAD VALIDATION REPORT ===")
    logger.info(f"Total Records: {total_records} (Expected: 7,043)")
    logger.info(f"Unique Customer IDs: {unique_ids} (Expected: 7,043)")
    logger.info(f"Total MRR: ${float(mrr_sum):,.2f} (Expected: $456,116.60)")
    logger.info(f"Total Cumulative Revenue: ${float(tc_sum):,.2f} (Expected: $16,056,168.70)")
    logger.info(f"Churn Distribution: Retained = {churn_counts.get('No')}, Churned = {churn_counts.get('Yes')}")
    
    assert total_records == 7043, "Row count mismatch!"
    assert unique_ids == 7043, "Duplicate IDs detected!"
    assert float(mrr_sum) == 456116.60, "MRR sum mismatch!"
    assert float(tc_sum) == 16056168.70, "TotalCharges sum mismatch!"
    logger.info("ALL POST-LOAD VALIDATION CHECKS PASSED PERFECTLY!")


def main():
    parser = argparse.ArgumentParser(description="Load cleaned Telco Customer Churn data into MySQL.")
    parser.add_argument("--host", default="localhost", help="MySQL Host")
    parser.add_argument("--port", type=int, default=3306, help="MySQL Port")
    parser.add_argument("--user", default="root", help="MySQL Username")
    parser.add_argument("--password", default="", help="MySQL Password")
    parser.add_argument("--database", default="customer_churn_db", help="MySQL Database Name")
    parser.add_argument("--csv", default="dataset/cleaned_telco_customer_churn.csv", help="Path to cleaned CSV")
    args = parser.parse_args()

    logger.info("=== STARTING MYSQL DATA LOADING PIPELINE ===")
    try:
        # Step 1: Connect to server without database to create DB
        conn_init = get_mysql_connection(args.host, args.port, args.user, args.password)
        execute_sql_file(conn_init, "sql/01_create_database.sql")
        conn_init.close()

        # Step 2: Connect to customer_churn_db to create tables
        conn_db = get_mysql_connection(args.host, args.port, args.user, args.password, database=args.database)
        execute_sql_file(conn_db, "sql/02_create_tables.sql")
        
        # Step 3: Load data
        load_cleaned_csv_to_mysql(conn_db, args.csv)
        
        # Step 4: Validate
        run_post_load_validation(conn_db)
        conn_db.close()
        logger.info("=== DATA LOADING COMPLETED SUCCESSFULLY ===")
    except Exception as e:
        logger.error(f"MySQL Loading Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
