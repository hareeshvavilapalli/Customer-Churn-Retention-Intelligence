// ==============================================================================
// Project: Customer Churn & Retention Intelligence System
// File: powerbi/power_query_transformations.m
// Description: Production Power Query M-Script for Data Ingestion & Transformation
// Author: Senior Data Analyst
// ==============================================================================

let
    // 1. Source CSV Ingestion with Multi-Path Fallback
    // Evaluates relative paths first, then falls back to repository root or absolute system path
    Source = try Csv.Document(
        File.Contents("..\dataset\cleaned_telco_customer_churn.csv"),
        [Delimiter=",", Columns=25, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ) otherwise try Csv.Document(
        File.Contents("dataset\cleaned_telco_customer_churn.csv"),
        [Delimiter=",", Columns=25, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ) otherwise Csv.Document(
        File.Contents("C:\Users\V.Leela prasad\OneDrive\Desktop\Customer-Churn-Retention-Intelligence\dataset\cleaned_telco_customer_churn.csv"),
        [Delimiter=",", Columns=25, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),

    // 2. Promote First Row as Headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // 3. Enforce Strict Column Data Types
    TypedTable = Table.TransformColumnTypes(PromotedHeaders, {
        {"customerID", type text},
        {"gender", type text},
        {"SeniorCitizen", Int64.Type},
        {"Partner", type text},
        {"Dependents", type text},
        {"tenure", Int64.Type},
        {"PhoneService", type text},
        {"MultipleLines", type text},
        {"InternetService", type text},
        {"OnlineSecurity", type text},
        {"OnlineBackup", type text},
        {"DeviceProtection", type text},
        {"TechSupport", type text},
        {"StreamingTV", type text},
        {"StreamingMovies", type text},
        {"Contract", type text},
        {"PaperlessBilling", type text},
        {"PaymentMethod", type text},
        {"MonthlyCharges", Currency.Type},
        {"TotalCharges", Currency.Type},
        {"Churn", type text},
        {"SeniorCitizen_Label", type text},
        {"tenure_group", type text},
        {"payment_category", type text},
        {"service_count", Int64.Type}
    }),

    // 4. Add Chronological Sort Key for Tenure Cohorts
    AddedTenureSort = Table.AddColumn(TypedTable, "Tenure_Group_Sort", each 
        if [tenure_group] = "0-12m" then 1
        else if [tenure_group] = "13-24m" then 2
        else if [tenure_group] = "25-36m" then 3
        else if [tenure_group] = "37-48m" then 4
        else if [tenure_group] = "49-60m" then 5
        else 6,
        Int64.Type
    ),

    // 5. Add Risk Scoring Columns in Power Query (Heuristic Flight Risk)
    AddedRiskScore = Table.AddColumn(AddedTenureSort, "Risk_Score", each 
        (if [Contract] = "Month-to-month" then 3 else 0) +
        (if [InternetService] = "Fiber optic" then 2 else 0) +
        (if [PaymentMethod] = "Electronic check" then 2 else 0) +
        (if [tenure] <= 12 then 2 else 0),
        Int64.Type
    ),

    AddedRiskTier = Table.AddColumn(AddedRiskScore, "Risk_Tier", each 
        if [Risk_Score] >= 7 then "1. Critical Risk (Score 7-9)"
        else if [Risk_Score] >= 4 then "2. Moderate Risk (Score 4-6)"
        else "3. Low Risk (Score 0-3)",
        type text
    ),

    AddedRiskTierSort = Table.AddColumn(AddedRiskTier, "Risk_Tier_Sort", each 
        if [Risk_Score] >= 7 then 1
        else if [Risk_Score] >= 4 then 2
        else 3,
        Int64.Type
    )
in
    AddedRiskTierSort
