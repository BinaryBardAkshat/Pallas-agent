# ML Model Evaluation

## Description
Systematically evaluate machine learning models: compute metrics, analyze errors, detect bias, compare baselines, and produce actionable improvement recommendations.

## When to Use
- After training a new model
- Comparing multiple model variants
- Investigating why a model is underperforming
- Pre-deployment validation

## Instructions
When evaluating an ML model:

**Step 1: Load and inspect**
```python
code_exec(code="""
import pandas as pd
# Load predictions and ground truth
df = pd.read_csv('predictions.csv')
print(df.head())
print(df.describe())
""")
```

**Step 2: Compute core metrics**
- Classification: accuracy, precision, recall, F1, AUC-ROC, confusion matrix
- Regression: MAE, RMSE, R², residual plot
- Ranking: NDCG, MAP, MRR

**Step 3: Error analysis**
- Which samples are most wrong?
- Are errors systematic (e.g., always wrong on a specific class)?
- Are there data quality issues in the error cases?

**Step 4: Bias and fairness check**
- Break down performance by demographic subgroups if applicable
- Check for label imbalance effects

**Step 5: Baseline comparison**
- Compare vs simple baselines (majority class, mean predictor, previous model version)
- Compute relative improvement %

**Step 6: Recommendations**
- Data: more data, better labels, feature engineering
- Model: architecture changes, hyperparameter tuning, ensembling
- Deployment: confidence thresholds, fallback strategies

## Examples
- "Evaluate my classification model on this test set"
- "Why is my model performing poorly on class X?"
- "Compare model v1 vs v2 performance"
