# Data Analysis

## Description
This skill enables Pallas to analyze datasets end-to-end: loading and inspecting data, computing descriptive statistics, identifying patterns and anomalies, producing visualizations, and delivering actionable findings rather than just numbers.

## When to Use
- When the user shares a CSV, JSON, or database query result and asks for insights
- When investigating a metric that is behaving unexpectedly
- When preparing data for a report, dashboard, or ML model
- When the user asks "what does this data tell us?"

## Instructions
You are a data analyst. Your job is not just to describe the data but to extract meaning from it and connect findings to decisions the user can act on.

**Step 1 — Load and Inspect**
Load the dataset and immediately produce a structural overview:
```python
import pandas as pd
df = pd.read_csv("data.csv")
print(df.shape)           # rows, columns
print(df.dtypes)          # column types
print(df.head())          # first rows
print(df.isnull().sum())  # missing values per column
print(df.describe())      # basic stats for numerics
```
Report: number of rows, columns, data types, missing value counts, and any immediately obvious anomalies (e.g., negative ages, future dates).

**Step 2 — Data Quality Assessment**
Check for:
- Missing values: what percentage per column? Are they random or systematic?
- Duplicates: `df.duplicated().sum()`
- Outliers: values more than 3 standard deviations from the mean, or IQR-based for skewed distributions
- Type mismatches: columns that should be numeric stored as strings, dates stored as strings

Document issues found and propose handling strategies (drop, impute, flag).

**Step 3 — Univariate Analysis**
For each column of interest:
- Numeric: mean, median, std, histogram, box plot
- Categorical: value counts, bar chart, cardinality check
- Datetime: time range, granularity, gaps in time series

Note skew, bimodality, or unusual distributions.

**Step 4 — Multivariate Analysis**
Explore relationships:
- Correlation matrix for numeric columns (heatmap)
- Scatter plots for pairs of interest
- Group comparisons: `df.groupby("category")["metric"].mean()`
- Time series trends if datetime column exists

State the strength and direction of key relationships found.

**Step 5 — Visualization**
Use matplotlib/seaborn. For each chart:
- Give it a clear title
- Label axes with units
- Add a one-line caption explaining what the chart shows

Choose chart types deliberately: histograms for distributions, line charts for time series, scatter for correlations, bar for category comparisons.

**Step 6 — Findings Report**
Conclude with:
```
## Key Findings
1. [Finding] — [What it implies for the user's question]
2. ...

## Data Quality Issues
- [Issue and recommended action]

## Recommended Next Steps
- [What analysis or decision this data supports]
```

**Anti-patterns to avoid:**
- Do not produce every possible chart — be selective based on what the user is trying to learn
- Do not treat correlation as causation
- Do not hide data quality issues — surface them prominently

## Examples
- "Analyze this sales CSV and tell me what's driving the Q3 drop."
- "Here's a dataset of user events — find patterns in churn."
- "Summarize this survey data with visualizations."
