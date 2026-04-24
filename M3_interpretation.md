# Milestone 3 Interpretation Memo

## Project Context
Research question: how do federal funds rate conditions relate to state-level unemployment over time?

Model A uses a two-way fixed effects panel design (state and date fixed effects) with a differential-exposure interaction so the effect is identified in the presence of time fixed effects.

## Model A Headline Result
Main coefficient (clustered SE):

- Fed Funds (lag 2) x High-Unemployment-State: $\hat\beta=-0.0042$, $p=0.032$

Economic interpretation in units:

- A 1 percentage-point increase in the federal funds rate (2-month lag) is associated with an additional 0.0042 percentage-point reduction in unemployment in higher-baseline-unemployment states relative to lower-baseline-unemployment states, conditional on state and time fixed effects and controls.

Supporting model terms:

- Unemployment lag(1): $0.9514$ ($p<0.001$), indicating strong monthly persistence.
- Recession x High-Unemployment-State: $0.1241$ ($p<0.001$), showing disproportionately higher unemployment for high-baseline states in recession periods.

Model fit:

- Within $R^2 = 0.8986$
- $N=20{,}544$

## Economic Interpretation and Causal Channels
The negative interaction estimate is consistent with heterogeneous transmission across states:

1. Financial conditions channel: rate changes alter borrowing conditions, with stronger labor-market adjustment in states more exposed to cyclical slack.
2. Policy-reaction/cycle channel: rates and unemployment both co-move with macro conditions, so differential exposure helps isolate relative effects rather than pure aggregate time shocks.
3. Persistence channel: high autoregressive unemployment dynamics imply policy-related effects are incremental and layered on top of strong inertia.

## Model B Summary (ML Comparison: OLS vs Random Forest)
Out-of-sample comparison (time split at 2018-10-01):

- OLS: Test $R^2=0.6359$, RMSE $=1.5000$
- Random Forest: Test $R^2=0.6277$, RMSE $=1.5168$

Key takeaway:

- Random Forest does not materially improve predictive performance over OLS in this setup. The simpler linear model remains competitive and easier to interpret.

## Diagnostics (Required)
1. Heteroskedasticity (Breusch-Pagan):
- LM stat $=66.85$, $p<0.001$
- Conclusion: heteroskedasticity is present; clustered standard errors are appropriate.

2. Multicollinearity (VIF):
- Fed Funds interaction: $1.44$
- Unemployment lag(1): $1.39$
- Recession interaction: $1.10$
- Conclusion: no problematic multicollinearity (all well below common thresholds such as 10).

3. Residual diagnostics:
- Residuals-vs-fitted and Q-Q plots were generated.
- Visual checks suggest reasonable fit with some tail departures, which is expected in macro-labor panel data.

## Robustness Checks (Required)
At least three checks were run:

1. Clustered vs unadjusted standard errors:
- Coefficient stable at $-0.0042$.
- Inference becomes more conservative under clustering: $p$ changes from $0.0079$ to $0.0320$.

2. Alternative lag structures for the key driver interaction:
- Lag 0: $-0.00547$ ($p=0.011$)
- Lag 1: $-0.00487$ ($p=0.018$)
- Lag 2: $-0.00423$ ($p=0.032$)
- Lag 3: $-0.00484$ ($p=0.022$)
- Conclusion: sign is consistently negative across tested lags, supporting robustness of direction.

3. Excluding COVID outlier months (2020-03 to 2020-05):
- Coefficient attenuates to $-0.00042$ ($p=0.775$).
- Conclusion: crisis months materially affect magnitude and significance; results are sensitive to extreme shock periods.

## Caveats and Identification Limits
1. Omitted variables: state-specific policy and industrial composition dynamics are not fully observed at monthly frequency.
2. Time-FE identification constraint: aggregate national variables are absorbed by time fixed effects; identified effects therefore come from differential exposure terms.
3. Dynamic panel concerns: including lagged dependent variables with FE can introduce small-sample bias (Nickell-type concerns), though long time dimension helps.
4. External validity: estimates are specific to the U.S. monthly state panel and may not generalize to other countries or frequencies.

## Output Files Generated
- `code/capstone_models.py`
- `results/tables/M3_regression_table.csv`
- `results/tables/M3_diagnostics_summary.csv`
- `results/tables/M3_vif_table.csv`
- `results/tables/M3_robustness_summary.csv`
- `results/tables/M3_robustness_lag_table.csv`
- `results/tables/M3_model_b_ml_comparison.csv`
- `results/tables/M3_modelA_fe_unadjusted_summary.txt`
- `results/tables/M3_modelA_fe_clustered_summary.txt`
- `results/figures/M3_residuals_vs_fitted.png`
- `results/figures/M3_qq_plot.png`
- `results/figures/M3_model_b_performance.png`
