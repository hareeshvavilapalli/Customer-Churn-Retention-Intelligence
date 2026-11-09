# Power BI recovery and validation notes

## Current project structure

The current Power BI project uses the modern PBIP/PBIR structure:

- `powerbi/Customer_Churn_Dashboard.pbip` — project entry point
- `powerbi/Customer_Churn_Dashboard.Report/definition.pbir` — report-to-semantic-model reference
- `powerbi/Customer_Churn_Dashboard.Report/definition/` — modern PBIR report pages and visual definitions
- `powerbi/Customer_Churn_Dashboard.SemanticModel/definition.pbism` — semantic-model descriptor
- `powerbi/Customer_Churn_Dashboard.SemanticModel/model.bim` — tabular model

The obsolete `Customer_Churn_Dashboard.Dataset` folder is not part of the current project and is excluded from this GitHub-ready archive.

## Repairs recorded

- Removed the conflicting legacy report descriptor at the report root; retained the modern PBIR definition.
- Removed the obsolete `definition.pbidataset` descriptor; retained `definition.pbism`.
- Removed unsupported `wordWrap` properties from the affected visual JSON files after Power BI Desktop reported schema warnings.
- Retained the three report pages and the current semantic model.

## User-side Power BI check

The project was opened in Power BI Desktop, and the user confirmed checking all three pages. This is a user-side GUI check; it is not an automated test performed in this archive-preparation environment. Recheck the report after extracting this archive.

## Data source portability

The model's Power Query source has used a local absolute CSV path in earlier project versions. Before refreshing on another machine, open Power BI Desktop, inspect the data source / Power Query source step, and point it to:

`dataset/cleaned_telco_customer_churn.csv`

Refresh the model and save only after confirming the refresh succeeds.

## Validation boundaries

- The project validation report records static checks. A passing static check count does not prove every application workflow works at runtime.
- MySQL scripts were prepared and syntax-reviewed, but a live MySQL Server execution was not confirmed.
- The customer risk score is a rule-based heuristic, not a trained ML model.
