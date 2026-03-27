# M2 EDA Summary

## Key Findings
- State unemployment and the federal funds rate have a moderate negative contemporaneous correlation ($r=-0.332$). This is best interpreted as business-cycle co-movement (policy endogeneity), not a structural claim that tighter policy lowers unemployment.
- State unemployment is strongly aligned with national unemployment ($r=0.772$), indicating common macro shocks dominate a large share of variation.
- Lag analysis shows the strongest absolute correlation at lag 0 months ($r=-0.332$), then decays at 1, 2, 3, 6, and 12 months. This supports a contemporaneous or short-lag M3 specification.
- Regional sensitivity to the federal funds rate is consistently negative (Midwest: -0.335, Northeast: -0.331, South: -0.348, West: -0.325), consistent with shared cyclical conditions across regions rather than direct expansionary effects of higher rates.
- Time-series and decomposition plots show clear crisis spikes and persistence around major downturns (especially 2008-2009 and 2020), implying nonlinearity and structural-period effects.

## Hypotheses for M3
### Hypothesis 1: Main Driver Effect
- Claim: In reduced-form contemporaneous data, higher federal funds rates are associated with lower unemployment because both variables respond to the business cycle; this does not imply a causal policy effect.
- Model specification:
  $$
  unemployment\_rate_{it} = \beta_0 + \beta_1\,federal\_funds\_rate_t + \alpha_i + \gamma_t + \varepsilon_{it}
  $$
- Expected sign: $\beta_1<0$ in naive/contemporaneous specifications; this coefficient is expected to attenuate, flip sign, or become unstable once stronger macro controls and timing structure are included.
- Mechanism: Central bank policy reacts to inflation/output conditions and labor-market tightness; omitted cyclical factors can induce a negative reduced-form correlation.

### Hypothesis 2: Control-Premium Effects
- Claim: Inflation, recession state, and macro labor controls materially improve fit beyond federal funds rate alone.
- Model specification:
  $$
  unemployment\_rate_{it} = \beta_0 + \beta_1\,federal\_funds\_rate_t + \beta_2\,inflation\_cpi_t + \beta_3\,recession\_indicator_t + \beta_4\,treasury\_10y\_yield_t + \alpha_i + \gamma_t + \varepsilon_{it}
  $$
- Expected signs:
  - recession_indicator: positive
- inflation_cpi: short-run Phillips-curve tradeoff may produce negative co-movement in some periods, but sign is sample- and regime-dependent
- treasury_10y_yield: ambiguous in reduced form because it blends expected growth and expected policy tightening
- Mechanism: Business-cycle state and financing conditions jointly shape labor demand.

### Hypothesis 3: Regional Heterogeneity
- Claim: The unemployment response to the federal funds rate differs by region.
- Model specification:
  $$
  unemployment\_rate_{it} = \beta_0 + \beta_1\,federal\_funds\_rate_t + \sum_r \delta_r\,(federal\_funds\_rate_t \times Region_{ir}) + \alpha_i + \gamma_t + \varepsilon_{it}
  $$
- Expected sign: Interaction terms are non-zero; South/Midwest may show larger absolute sensitivity than West/Northeast in this sample.
- Mechanism: Industrial composition, labor mobility, and credit exposure vary across regions.

## Data Quality Flags and M3 Mitigations
- Missingness: Several macro controls have ~44.44% missingness in early periods (for example total_nonfarm_employment, civilian_labor_force, manufacturing_employment).
  - Mitigation: Use a complete-case baseline plus robustness checks on restricted post-coverage windows; report $N$ for each model.
- Outliers: Unemployment has extreme observations (99th percentile = 11.4, max = 30.5), likely crisis-linked.
  - Mitigation: Winsorized sensitivity checks and crisis-period indicator interactions.
- Heteroskedasticity risk: Group boxplots show unequal spread across regions.
  - Mitigation: Use heteroskedasticity-robust or clustered standard errors (state-clustered).
- Multicollinearity risk: Correlation heatmap indicates some macro controls are strongly co-moving.
  - Mitigation: Check VIFs, avoid redundant controls, and compare nested models (parsimonious vs. full specification).

## Econometric Readiness Notes
- Identification caution: These EDA patterns are descriptive and may reflect policy endogeneity over the business cycle.
- M3 adjustment: Include time fixed effects, recession controls, and lag/lead structure (or dynamic terms) to separate cyclical co-movement from plausible transmission timing.
- Inference plan: Report heteroskedasticity-robust and state-clustered standard errors as a sensitivity check.

## Files Produced for M2
- capstone_eda.ipynb (runs top-to-bottom, includes required visualizations and captions)
- results/figures/M2_plot1_correlation_heatmap.png
- results/figures/M2_plot2_outcome_timeseries.png
- results/figures/M2_plot3_dual_axis_unemp_fedfunds.png
- results/figures/M2_plot4_lagged_effects.png
- results/figures/M2_plot5_group_boxplot_region.png
- results/figures/M2_plot6_group_sensitivity_region.png
- results/figures/M2_plot7_scatter_controls.png
- results/figures/M2_plot8_decomposition.png
