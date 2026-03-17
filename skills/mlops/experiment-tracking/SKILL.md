# ML Experiment Tracking

## Description
This skill enables Pallas to systematically track machine learning experiments: logging hyperparameters, metrics, and artifacts; comparing runs across configurations; identifying the best-performing model; and producing clear experiment reports that support reproducible research.

## When to Use
- When starting a new round of model training and wanting to track results
- When comparing multiple training runs to select the best configuration
- When preparing a report on model development history for a team
- When reproducing a previous experiment result

## Instructions
You are an MLOps engineer responsible for maintaining a rigorous, reproducible experiment log. Every experiment that cannot be reproduced and compared is wasted effort.

**Step 1 — Experiment Setup**
Before running any experiment, define and record:
- **Experiment ID**: unique identifier (use timestamp + short description, e.g., `20250317_lr_sweep`)
- **Hypothesis**: what you expect this configuration to improve and why
- **Changes from baseline**: what is different about this run vs. the current best
- **Dataset version**: exact dataset split, hash, or version tag used
- **Environment**: Python version, key library versions (PyTorch, TF, sklearn), hardware

Never start a run without recording these. "I'll remember it" is not a tracking strategy.

**Step 2 — Hyperparameter Logging**
Log every parameter that could affect the result:
- Model architecture parameters (hidden size, num layers, dropout rate)
- Training parameters (learning rate, batch size, epochs, optimizer, scheduler)
- Data preprocessing parameters (normalization strategy, augmentation settings)
- Regularization settings

Use a structured config object or YAML file, not ad-hoc code. Log the full config, not just the changed values.

**Step 3 — Metrics Logging**
Log at the right granularity:
- Per epoch: train loss, validation loss, primary metric
- Final: test set metrics, training time, peak GPU memory
- Use consistent metric names across all runs — `val_f1` not `validation_f1` in some runs and `val_f1_score` in others

If using a tracking tool (MLflow, W&B, Comet), use the standard logging API. If logging manually, use a structured format:

```json
{
  "experiment_id": "20250317_lr_sweep",
  "config": {"lr": 0.001, "batch_size": 32, ...},
  "metrics": {"val_f1": 0.847, "test_f1": 0.839, "train_time_min": 14.2}
}
```

**Step 4 — Artifact Tracking**
Save and version:
- Model checkpoint (best validation metric, not just final epoch)
- Tokenizer / preprocessor state
- Training curves plot
- Confusion matrix on test set

Store artifacts with a reference to the experiment ID so they can be traced back.

**Step 5 — Experiment Comparison**
When multiple runs exist, produce a comparison table sorted by primary metric:

```
| Experiment ID       | LR    | Batch | Val F1 | Test F1 | Train Time |
|---------------------|-------|-------|--------|---------|------------|
| 20250317_baseline   | 0.001 | 32    | 0.821  | 0.815   | 14.2 min   |
| 20250317_lr_sweep_1 | 0.003 | 32    | 0.847  | 0.839   | 13.8 min   |
| 20250317_lr_sweep_2 | 0.0001| 32    | 0.803  | 0.797   | 15.1 min   |
```

Highlight the best run per metric. Note any experiments that were stopped early or produced anomalous results (NaN loss, evaluation divergence).

**Step 6 — Best Model Selection and Handoff**
Document the selected model with:
- Experiment ID and config
- Validation and test metrics
- Why it was selected over alternatives
- Known limitations or failure modes observed during evaluation
- Path to model artifact

**Anti-patterns:**
- Never overwrite previous experiment results — always create a new experiment ID
- Do not cherry-pick metrics — report the full set, even the ones that look bad
- Do not compare models trained on different dataset splits — standardize the eval set

## Examples
- "Log this training run and compare it to the previous two experiments."
- "Which of my last 5 training runs had the best F1/training-time tradeoff?"
- "Generate an experiment report for this model before we deploy it."
