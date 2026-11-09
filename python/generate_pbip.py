"""
Safe Minimal Repair for Power BI Project (.pbip)
Removes uncompilable relative File.Contents calls and expressions parameter from model.bim.
Restores the exact, verified TMSL model structure that opened successfully in commit a3a18d5,
while preserving all layout, card unstacking, slicer widening, and Page 3 action plan fixes in report.json.
"""

import json
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
POWERBI_DIR = BASE_DIR / "powerbi"
CSV_PATH = "C:\\Users\\V.Leela prasad\\OneDrive\\Desktop\\Customer-Churn-Retention-Intelligence\\dataset\\cleaned_telco_customer_churn.csv"
PBIP_NAME = "Customer_Churn_Dashboard"

SEMANTIC_MODEL_DIR = POWERBI_DIR / f"{PBIP_NAME}.SemanticModel"
DATASET_DIR = POWERBI_DIR / f"{PBIP_NAME}.Dataset"
REPORT_DIR = POWERBI_DIR / f"{PBIP_NAME}.Report"

def make_hex_id():
    return uuid.uuid4().hex[:20]

def generate_pbip_descriptor():
    content = {
        "version": "1.0",
        "artifacts": [
            {
                "report": {
                    "path": f"{PBIP_NAME}.Report"
                }
            }
        ],
        "settings": {
            "enableAutoAuth": True
        }
    }
    path = POWERBI_DIR / f"{PBIP_NAME}.pbip"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"[OK] Generated {path}")

def generate_pbism(target_dir):
    content = {
        "version": "4.2",
        "settings": {}
    }
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / "definition.pbism"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"[OK] Generated {path}")

def generate_pbidataset(target_dir):
    content = {
        "version": "1.0",
        "settings": {}
    }
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / "definition.pbidataset"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"[OK] Generated {path}")

def get_model_bim_content():
    # Pure, valid Power Query M expression with absolute Windows path (proven working in commit a3a18d5)
    m_expression = [
        "let",
        f'    Source = Csv.Document(File.Contents("{CSV_PATH}"), [Delimiter=",", Columns=25, Encoding=65001, QuoteStyle=QuoteStyle.None]),',
        "    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
        "    TypedTable = Table.TransformColumnTypes(PromotedHeaders, {",
        '        {"customerID", type text},',
        '        {"gender", type text},',
        '        {"SeniorCitizen", Int64.Type},',
        '        {"Partner", type text},',
        '        {"Dependents", type text},',
        '        {"tenure", Int64.Type},',
        '        {"PhoneService", type text},',
        '        {"MultipleLines", type text},',
        '        {"InternetService", type text},',
        '        {"OnlineSecurity", type text},',
        '        {"OnlineBackup", type text},',
        '        {"DeviceProtection", type text},',
        '        {"TechSupport", type text},',
        '        {"StreamingTV", type text},',
        '        {"StreamingMovies", type text},',
        '        {"Contract", type text},',
        '        {"PaperlessBilling", type text},',
        '        {"PaymentMethod", type text},',
        '        {"MonthlyCharges", Currency.Type},',
        '        {"TotalCharges", Currency.Type},',
        '        {"Churn", type text},',
        '        {"SeniorCitizen_Label", type text},',
        '        {"tenure_group", type text},',
        '        {"payment_category", type text},',
        '        {"service_count", Int64.Type}',
        "    }),",
        '    AddedTenureSort = Table.AddColumn(TypedTable, "Tenure_Group_Sort", each ',
        '        if [tenure_group] = "0-12m" then 1',
        '        else if [tenure_group] = "13-24m" then 2',
        '        else if [tenure_group] = "25-36m" then 3',
        '        else if [tenure_group] = "37-48m" then 4',
        '        else if [tenure_group] = "49-60m" then 5',
        "        else 6,",
        "        Int64.Type",
        "    ),",
        '    AddedRiskScore = Table.AddColumn(AddedTenureSort, "Risk_Score", each ',
        '        (if [Contract] = "Month-to-month" then 3 else 0) +',
        '        (if [InternetService] = "Fiber optic" then 2 else 0) +',
        '        (if [PaymentMethod] = "Electronic check" then 2 else 0) +',
        "        (if [tenure] <= 12 then 2 else 0),",
        "        Int64.Type",
        "    ),",
        '    AddedRiskTier = Table.AddColumn(AddedRiskScore, "Risk_Tier", each ',
        '        if [Risk_Score] >= 7 then "1. Critical Risk (Score 7-9)"',
        '        else if [Risk_Score] >= 4 then "2. Moderate Risk (Score 4-6)"',
        '        else "3. Low Risk (Score 0-3)",',
        "        type text",
        "    ),",
        '    AddedRiskTierSort = Table.AddColumn(AddedRiskTier, "Risk_Tier_Sort", each ',
        "        if [Risk_Score] >= 7 then 1",
        "        else if [Risk_Score] >= 4 then 2",
        "        else 3,",
        "        Int64.Type",
        "    )",
        "in",
        "    AddedRiskTierSort"
    ]

    columns = [
        {"name": "customerID", "dataType": "string", "sourceColumn": "customerID"},
        {"name": "gender", "dataType": "string", "sourceColumn": "gender"},
        {"name": "SeniorCitizen", "dataType": "int64", "sourceColumn": "SeniorCitizen"},
        {"name": "Partner", "dataType": "string", "sourceColumn": "Partner"},
        {"name": "Dependents", "dataType": "string", "sourceColumn": "Dependents"},
        {"name": "tenure", "dataType": "int64", "sourceColumn": "tenure"},
        {"name": "PhoneService", "dataType": "string", "sourceColumn": "PhoneService"},
        {"name": "MultipleLines", "dataType": "string", "sourceColumn": "MultipleLines"},
        {"name": "InternetService", "dataType": "string", "sourceColumn": "InternetService"},
        {"name": "OnlineSecurity", "dataType": "string", "sourceColumn": "OnlineSecurity"},
        {"name": "OnlineBackup", "dataType": "string", "sourceColumn": "OnlineBackup"},
        {"name": "DeviceProtection", "dataType": "string", "sourceColumn": "DeviceProtection"},
        {"name": "TechSupport", "dataType": "string", "sourceColumn": "TechSupport"},
        {"name": "StreamingTV", "dataType": "string", "sourceColumn": "StreamingTV"},
        {"name": "StreamingMovies", "dataType": "string", "sourceColumn": "StreamingMovies"},
        {"name": "Contract", "dataType": "string", "sourceColumn": "Contract"},
        {"name": "PaperlessBilling", "dataType": "string", "sourceColumn": "PaperlessBilling"},
        {"name": "PaymentMethod", "dataType": "string", "sourceColumn": "PaymentMethod"},
        {"name": "MonthlyCharges", "dataType": "decimal", "sourceColumn": "MonthlyCharges", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00"},
        {"name": "TotalCharges", "dataType": "decimal", "sourceColumn": "TotalCharges", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00"},
        {"name": "Churn", "dataType": "string", "sourceColumn": "Churn"},
        {"name": "SeniorCitizen_Label", "dataType": "string", "sourceColumn": "SeniorCitizen_Label"},
        {"name": "tenure_group", "dataType": "string", "sourceColumn": "tenure_group", "sortByColumn": "Tenure_Group_Sort"},
        {"name": "payment_category", "dataType": "string", "sourceColumn": "payment_category"},
        {"name": "service_count", "dataType": "int64", "sourceColumn": "service_count"},
        {"name": "Tenure_Group_Sort", "dataType": "int64", "sourceColumn": "Tenure_Group_Sort", "isHidden": True},
        {"name": "Risk_Score", "dataType": "int64", "sourceColumn": "Risk_Score"},
        {"name": "Risk_Tier", "dataType": "string", "sourceColumn": "Risk_Tier", "sortByColumn": "Risk_Tier_Sort"},
        {"name": "Risk_Tier_Sort", "dataType": "int64", "sourceColumn": "Risk_Tier_Sort", "isHidden": True}
    ]

    measures = [
        {"name": "Total Customers", "expression": "COUNTROWS('CustomerChurn')", "formatString": "#,##0", "displayFolder": "1. Volume & Churn"},
        {"name": "Churned Customers", "expression": "CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "#,##0", "displayFolder": "1. Volume & Churn"},
        {"name": "Retained Customers", "expression": "CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Churn] = \"No\")", "formatString": "#,##0", "displayFolder": "1. Volume & Churn"},
        {"name": "Churn Rate %", "expression": "DIVIDE([Churned Customers], [Total Customers], 0)", "formatString": "0.00%", "displayFolder": "1. Volume & Churn"},
        {"name": "Retention Rate %", "expression": "DIVIDE([Retained Customers], [Total Customers], 0)", "formatString": "0.00%", "displayFolder": "1. Volume & Churn"},
        {"name": "Total Monthly Revenue (MRR)", "expression": "SUM('CustomerChurn'[MonthlyCharges])", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Lost MRR", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Retained MRR", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Churn] = \"No\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Lost MRR %", "expression": "DIVIDE([Lost MRR], [Total Monthly Revenue (MRR)], 0)", "formatString": "0.00%", "displayFolder": "2. Financial & Revenue"},
        {"name": "Total Cumulative Revenue", "expression": "SUM('CustomerChurn'[TotalCharges])", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Monthly Charges", "expression": "AVERAGE('CustomerChurn'[MonthlyCharges])", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Monthly Charges - Churned", "expression": "CALCULATE(AVERAGE('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Monthly Charges - Retained", "expression": "CALCULATE(AVERAGE('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Churn] = \"No\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Monthly Charge Delta", "expression": "[Average Monthly Charges - Churned] - [Average Monthly Charges - Retained]", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Tenure", "expression": "AVERAGE('CustomerChurn'[tenure])", "formatString": "0.0", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Tenure - Churned", "expression": "CALCULATE(AVERAGE('CustomerChurn'[tenure]), 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "0.0", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Tenure - Retained", "expression": "CALCULATE(AVERAGE('CustomerChurn'[tenure]), 'CustomerChurn'[Churn] = \"No\")", "formatString": "0.0", "displayFolder": "2. Financial & Revenue"},
        {"name": "Average Total Charges", "expression": "AVERAGE('CustomerChurn'[TotalCharges])", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Customer Lifetime Value (LTV)", "expression": "[Average Total Charges]", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "2. Financial & Revenue"},
        {"name": "Revenue at Risk (Critical MRR At Stake)", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Risk_Tier] = \"1. Critical Risk (Score 7-9)\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "3. Risk Intelligence"},
        {"name": "Realized Lost MRR (Critical)", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Risk_Tier] = \"1. Critical Risk (Score 7-9)\", 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "3. Risk Intelligence"},
        {"name": "Critical Risk Customer Count", "expression": "CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Risk_Tier] = \"1. Critical Risk (Score 7-9)\")", "formatString": "#,##0", "displayFolder": "3. Risk Intelligence"},
        {"name": "Moderate Risk Customer Count", "expression": "CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Risk_Tier] = \"2. Moderate Risk (Score 4-6)\")", "formatString": "#,##0", "displayFolder": "3. Risk Intelligence"},
        {"name": "Low Risk Customer Count", "expression": "CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Risk_Tier] = \"3. Low Risk (Score 0-3)\")", "formatString": "#,##0", "displayFolder": "3. Risk Intelligence"},
        {"name": "Critical Risk Churn Rate %", "expression": "DIVIDE(CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Risk_Tier] = \"1. Critical Risk (Score 7-9)\", 'CustomerChurn'[Churn] = \"Yes\"), [Critical Risk Customer Count], 0)", "formatString": "0.00%", "displayFolder": "3. Risk Intelligence"},
        {"name": "Critical Risk Share of Total Churn %", "expression": "DIVIDE(CALCULATE(COUNTROWS('CustomerChurn'), 'CustomerChurn'[Risk_Tier] = \"1. Critical Risk (Score 7-9)\", 'CustomerChurn'[Churn] = \"Yes\"), [Churned Customers], 0)", "formatString": "0.00%", "displayFolder": "3. Risk Intelligence"},
        {"name": "High ARPU Lost MRR", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[MonthlyCharges] >= 89.85, 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "4. Segment Losses"},
        {"name": "Fiber Optic Lost MRR", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[InternetService] = \"Fiber optic\", 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "4. Segment Losses"},
        {"name": "Month to Month Lost MRR", "expression": "CALCULATE(SUM('CustomerChurn'[MonthlyCharges]), 'CustomerChurn'[Contract] = \"Month-to-month\", 'CustomerChurn'[Churn] = \"Yes\")", "formatString": "\\$#,0.00;(\\$#,0.00);\\$#,0.00", "displayFolder": "4. Segment Losses"}
    ]

    return {
        "name": "Customer_Churn_Dashboard",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "collation": "Latin1_General_100_BIN2_UTF8",
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-US",
            "tables": [
                {
                    "name": "CustomerChurn",
                    "columns": columns,
                    "partitions": [
                        {
                            "name": "CustomerChurn",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": m_expression
                            }
                        }
                    ],
                    "measures": measures
                }
            ],
            "annotations": [
                {
                    "name": "PBI_QueryOrder",
                    "value": "[\"CustomerChurn\"]"
                }
            ]
        }
    }

def generate_model_bim(target_dir):
    content = get_model_bim_content()
    target_dir.mkdir(parents=True, exist_ok=True)
    path = target_dir / "model.bim"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"[OK] Generated {path}")

def generate_pbir():
    content = {
        "version": "1.0",
        "datasetReference": {
            "byPath": {
                "path": f"../{PBIP_NAME}.SemanticModel"
            }
        }
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / "definition.pbir"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
    print(f"[OK] Generated {path}")

def make_card(x, y, w, h, measure_name, title, font_size="22D"):
    cid = make_hex_id()
    config = {
        "name": cid,
        "layouts": [{"id": 0, "position": {"x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h)}}],
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Values": [{"queryRef": f"CustomerChurn.{measure_name}"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "c", "Entity": "CustomerChurn", "Type": 0}],
                "Select": [
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": measure_name
                        },
                        "Name": f"CustomerChurn.{measure_name}"
                    }
                ]
            },
            "objects": {
                "labels": [
                    {
                        "properties": {
                            "fontSize": {"expr": {"Literal": {"Value": font_size}}},
                            "labelDisplayUnits": {"expr": {"Literal": {"Value": "0D"}}}
                        }
                    }
                ],
                "categoryLabels": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "false"}}}
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h),
        "config": json.dumps(config),
        "filters": "[]"
    }

def make_slicer(x, y, w, h, col_name, title):
    cid = make_hex_id()
    config = {
        "name": cid,
        "layouts": [{"id": 0, "position": {"x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h)}}],
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [{"queryRef": f"CustomerChurn.{col_name}"}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "c", "Entity": "CustomerChurn", "Type": 0}],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": col_name
                        },
                        "Name": f"CustomerChurn.{col_name}"
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h),
        "config": json.dumps(config),
        "filters": "[]"
    }

def make_chart(visual_type, x, y, w, h, category_col, measure_name, title):
    cid = make_hex_id()
    if visual_type in ["clusteredBarChart", "clusteredColumnChart", "donutChart"]:
        projections = {
            "Category": [{"queryRef": f"CustomerChurn.{category_col}"}],
            "Y": [{"queryRef": f"CustomerChurn.{measure_name}"}]
        }
    else:
        projections = {
            "Category": [{"queryRef": f"CustomerChurn.{category_col}"}],
            "Values": [{"queryRef": f"CustomerChurn.{measure_name}"}]
        }

    config = {
        "name": cid,
        "layouts": [{"id": 0, "position": {"x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h)}}],
        "singleVisual": {
            "visualType": visual_type,
            "projections": projections,
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "c", "Entity": "CustomerChurn", "Type": 0}],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": category_col
                        },
                        "Name": f"CustomerChurn.{category_col}"
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": measure_name
                        },
                        "Name": f"CustomerChurn.{measure_name}"
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h),
        "config": json.dumps(config),
        "filters": "[]"
    }

def make_textbox(x, y, w, h, title, bullets):
    cid = make_hex_id()
    
    paragraphs = []
    paragraphs.append({
        "textRuns": [
            {
                "value": f"{title}\n\n"
            }
        ]
    })
    
    for idx, (heading, text) in enumerate(bullets, start=1):
        paragraphs.append({
            "textRuns": [
                {
                    "value": f"{idx}. {heading}: {text}\n\n"
                }
            ]
        })

    config = {
        "name": cid,
        "layouts": [{"id": 0, "position": {"x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h)}}],
        "singleVisual": {
            "visualType": "textbox",
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": paragraphs
                        }
                    }
                ]
            },
            "vcObjects": {
                "title": [
                    {
                        "properties": {
                            "show": {"expr": {"Literal": {"Value": "true"}}},
                            "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                            "fontSize": {"expr": {"Literal": {"Value": "11D"}}}
                        }
                    }
                ]
            }
        }
    }
    return {
        "x": float(x), "y": float(y), "z": 0.0, "width": float(w), "height": float(h),
        "config": json.dumps(config),
        "filters": "[]"
    }

def generate_report_json():
    # Page 1: Executive Overview
    page1 = [
        make_card(20, 15, 195, 90, "Total Customers", "Total Customers", "22D"),
        make_card(225, 15, 195, 90, "Churned Customers", "Churned Customers", "22D"),
        make_card(430, 15, 195, 90, "Churn Rate %", "Churn Rate %", "22D"),
        make_card(635, 15, 195, 90, "Retention Rate %", "Retention Rate %", "22D"),
        make_card(840, 15, 205, 90, "Total Monthly Revenue (MRR)", "Total MRR", "20D"),
        make_card(1055, 15, 205, 90, "Lost MRR", "Lost MRR", "20D"),

        make_slicer(20, 120, 225, 175, "Contract", "Contract Filter"),
        make_slicer(20, 310, 225, 185, "PaymentMethod", "Payment Method Filter"),
        make_slicer(20, 510, 225, 185, "SeniorCitizen_Label", "Demographic Filter"),

        make_chart("donutChart", 260, 120, 345, 275, "Churn", "Total Customers", "Churn Distribution (Yes vs No)"),
        make_chart("clusteredBarChart", 620, 120, 640, 275, "Contract", "Churn Rate %", "Churn Rate % by Contract Type"),
        make_chart("clusteredColumnChart", 260, 410, 500, 285, "tenure_group", "Churned Customers", "Churn Volume by Tenure Cohort"),
        make_chart("clusteredBarChart", 775, 410, 485, 285, "payment_category", "Lost MRR", "Lost MRR by Payment Category ($)")
    ]

    # Page 2: Customer Churn Analysis
    page2 = [
        make_slicer(20, 15, 235, 85, "Contract", "Contract Filter"),
        make_slicer(265, 15, 235, 85, "InternetService", "Internet Service Filter"),
        make_slicer(510, 15, 235, 85, "tenure_group", "Tenure Cohort Filter"),
        make_card(755, 15, 245, 85, "Churn Rate %", "Overall Churn Rate", "22D"),
        make_card(1010, 15, 250, 85, "Lost MRR", "Total Lost MRR", "20D"),

        make_chart("clusteredBarChart", 20, 115, 395, 275, "Contract", "Churn Rate %", "1. Churn by Contract Type"),
        make_chart("clusteredColumnChart", 430, 115, 415, 275, "tenure_group", "Churn Rate %", "2. Churn by Tenure Cohort"),
        make_chart("clusteredBarChart", 860, 115, 400, 275, "InternetService", "Churn Rate %", "3. Churn by Internet Service"),

        make_chart("clusteredBarChart", 20, 405, 395, 290, "PaymentMethod", "Churn Rate %", "4. Churn by Payment Method"),
        make_chart("clusteredColumnChart", 430, 405, 415, 290, "service_count", "Churn Rate %", "5. Churn by Bundled Services"),
        make_chart("clusteredBarChart", 860, 405, 400, 290, "TechSupport", "Churn Rate %", "6. Churn by Tech Support Status")
    ]

    # Page 3: Revenue & Retention Intelligence
    action_plan_bullets = [
        ("Contract Term Incentives", "Month-to-month contracts account for $122.9K (88.3%) of Lost MRR. Deploy a 10% annual commitment discount or streaming perk to transition month-to-month subscribers."),
        ("First-Year Onboarding Cadence", "55.5% of churn events occur in months 0-12 (47.4% churn rate). Establish automated Day-14, 30, 60, and 90 proactive check-ins to stabilize new subscriber cohorts."),
        ("Fiber Optic Support Shield", "Fiber accounts represent $118.7K MRR lost (41.9% churn). Bundling Tech Support reduces churn from 41.6% to 15.2%. Automatically package free Tech Support with premium tiers."),
        ("Auto-Pay Switch Campaign", "Electronic check users churn at 45.3% vs 15.2% for credit card auto-pay. Offer a $5/month statement credit to migrate subscribers to automated recurring payments.")
    ]

    page3 = [
        make_card(20, 15, 295, 95, "Revenue at Risk (Critical MRR At Stake)", "Critical Revenue At Stake", "20D"),
        make_card(325, 15, 295, 95, "Realized Lost MRR (Critical)", "Realized Lost MRR (Critical)", "20D"),
        make_card(630, 15, 295, 95, "Critical Risk Customer Count", "Critical Flight Risk Customers", "22D"),
        make_card(935, 15, 325, 95, "Critical Risk Churn Rate %", "Critical Cohort Churn Rate", "22D"),

        make_chart("donutChart", 20, 125, 400, 285, "Risk_Tier", "Total Customers", "Risk-Tier Customer Composition (Volume & Share)"),
        make_chart("clusteredColumnChart", 435, 125, 415, 285, "tenure_group", "Lost MRR", "Lost MRR by Tenure Cohort ($)"),
        make_chart("clusteredBarChart", 865, 125, 395, 285, "InternetService", "Lost MRR", "Lost MRR by Internet Service ($)"),

        make_slicer(20, 425, 235, 275, "Risk_Tier", "Risk Tier Filter"),
        make_slicer(270, 425, 235, 275, "Contract", "Contract Filter"),

        make_textbox(520, 425, 740, 275, "Executive Retention Playbook & Strategic Action Plan", action_plan_bullets)
    ]

    report_content = {
        "config": json.dumps({
            "version": "5.50",
            "themeCollection": {
                "baseTheme": {
                    "name": "CY19SU06",
                    "version": "5.50",
                    "type": 2
                }
            },
            "activeSectionIndex": 0,
            "defaultDrillFilterOtherVisuals": True
        }),
        "layoutOptimization": 0,
        "sections": [
            {
                "name": "ReportSection1",
                "displayName": "Executive Overview",
                "filters": "[]",
                "ordinal": 0,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": page1
            },
            {
                "name": "ReportSection2",
                "displayName": "Customer Churn Analysis",
                "filters": "[]",
                "ordinal": 1,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": page2
            },
            {
                "name": "ReportSection3",
                "displayName": "Revenue & Retention Intelligence",
                "filters": "[]",
                "ordinal": 2,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": page3
            }
        ]
    }

    path = REPORT_DIR / "report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report_content, f, indent=2)
    print(f"[OK] Generated {path}")

def main():
    print("=== EXECUTING SAFE MINIMAL PBIP REPAIR ===")
    generate_pbip_descriptor()
    generate_pbism(SEMANTIC_MODEL_DIR)
    generate_model_bim(SEMANTIC_MODEL_DIR)
    generate_pbidataset(DATASET_DIR)
    generate_model_bim(DATASET_DIR)
    generate_pbir()
    generate_report_json()
    print("=== REPAIR COMPLETE ===")

if __name__ == "__main__":
    main()
