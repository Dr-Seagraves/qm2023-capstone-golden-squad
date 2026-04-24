"""
QM 2023 Capstone: Milestone 3 Econometric Models
Team: Golden Squad
Members: Team Submission
Date: 2026-04-20

This script estimates panel regression models to identify effects of interest-rate
conditions on state-level unemployment. It implements:
1) Model A: Fixed Effects panel regression (required)
2) Model B: OLS vs Random Forest predictive comparison
3) Required diagnostics and robustness checks

Outputs are saved to results/tables and results/figures using config_paths.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _maybe_reexec_in_venv() -> None:
    """Re-run this script in project .venv to avoid system-Python dependency errors."""
    project_root = Path(__file__).resolve().parents[1]
    venv_python = (project_root / ".venv" / "bin" / "python").absolute()

    # Prevent re-exec loops and honor manual opt-out for debugging.
    if os.environ.get("QM2023_REEXEC") == "1":
        return
    if os.environ.get("QM2023_SKIP_VENV_REEXEC") == "1":
        return
    if not venv_python.exists():
        return

    current_python = Path(sys.executable).absolute()
    if current_python == venv_python:
        return

    print(
        f"[info] Detected interpreter '{current_python}'. Re-running in project venv: '{venv_python}'.",
        file=sys.stderr,
    )
    os.execve(
        str(venv_python),
        [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]],
        {**os.environ, "QM2023_REEXEC": "1"},
    )


_maybe_reexec_in_venv()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from linearmodels.panel import PanelOLS
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Allow importing shared path config when running as: python code/capstone_models.py
sys.path.insert(0, str(Path(__file__).parent))
from config_paths import FIGURES_DIR, FINAL_DATA_DIR, TABLES_DIR


def significance_stars(p_value: float) -> str:
    """Return standard significance stars for table display."""
    if pd.isna(p_value):
        return ""
    if p_value < 0.01:
        return "***"
    if p_value < 0.05:
        return "**"
    if p_value < 0.10:
        return "*"
    return ""


def load_data() -> pd.DataFrame:
    """Load the enhanced panel and prepare core date/state fields."""
    panel_path = FINAL_DATA_DIR / "analysis_panel_enhanced.csv"
    if not panel_path.exists():
        raise FileNotFoundError(
            f"Missing required input dataset: {panel_path}. "
            "Run code/merge_final_panel_enhanced.py first."
        )

    df = pd.read_csv(panel_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["state", "date"]).reset_index(drop=True)
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer lag and interaction variables needed for identification and robustness."""
    out = df.copy()

    # State-specific dynamics
    out["unemployment_lag1"] = out.groupby("state")["unemployment_rate"].shift(1)

    # Federal funds lags by state panel index (same national series replicated across states)
    for lag in [0, 1, 2, 3]:
        out[f"fedfunds_lag{lag}"] = out.groupby("state")["federal_funds_rate"].shift(lag)

    # Exposure proxy: states with above-median long-run unemployment are more rate-sensitive.
    baseline_state_mean = out.groupby("state")["unemployment_rate"].transform("mean")
    median_baseline = baseline_state_mean.median()
    out["high_unemp_state"] = (baseline_state_mean >= median_baseline).astype(int)

    # Interaction terms avoid perfect collinearity with time fixed effects.
    for lag in [0, 1, 2, 3]:
        out[f"fedfunds_lag{lag}_x_high_unemp"] = (
            out[f"fedfunds_lag{lag}"] * out["high_unemp_state"]
        )

    # Additional interaction control that varies by state and time.
    out["recession_x_high_unemp"] = out["recession_indicator"] * out["high_unemp_state"]

    return out


def prepare_model_data(df: pd.DataFrame, fed_lag: int = 2) -> pd.DataFrame:
    """Create analysis frame for Model A with chosen lag."""
    required_cols = [
        "unemployment_rate",
        f"fedfunds_lag{fed_lag}_x_high_unemp",
        "unemployment_lag1",
        "recession_x_high_unemp",
        "state",
        "date",
    ]

    data = df[required_cols].dropna().copy()
    data = data.set_index(["state", "date"]).sort_index()
    return data


def fit_fixed_effects(data: pd.DataFrame, fed_lag: int = 2, clustered: bool = True):
    """Estimate two-way fixed effects model with optional clustered standard errors."""
    y = data["unemployment_rate"]
    x_cols = [
        f"fedfunds_lag{fed_lag}_x_high_unemp",
        "unemployment_lag1",
        "recession_x_high_unemp",
    ]
    X = data[x_cols]

    model = PanelOLS(
        y,
        X,
        entity_effects=True,
        time_effects=True,
        drop_absorbed=True,
    )

    if clustered:
        result = model.fit(cov_type="clustered", cluster_entity=True)
    else:
        result = model.fit(cov_type="unadjusted")

    return result, x_cols


def model_b_ml_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """Compare out-of-sample predictive performance of OLS vs Random Forest."""
    work = df.copy()
    work["year"] = work["date"].dt.year
    work["month"] = work["date"].dt.month

    features = [
        "federal_funds_rate",
        "national_unemployment_rate",
        "inflation_cpi",
        "recession_indicator",
        "treasury_10y_yield",
        "unemployment_lag1",
    ]
    keep = ["unemployment_rate", "state", "date"] + features
    work = work[keep].dropna().copy()

    # Time-based split avoids look-ahead bias.
    cutoff = work["date"].quantile(0.8)
    train = work[work["date"] <= cutoff].copy()
    test = work[work["date"] > cutoff].copy()

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    train_states = encoder.fit_transform(train[["state"]])
    test_states = encoder.transform(test[["state"]])

    X_train_num = train[features].to_numpy()
    X_test_num = test[features].to_numpy()
    X_train = np.hstack([X_train_num, train_states])
    X_test = np.hstack([X_test_num, test_states])
    y_train = train["unemployment_rate"].to_numpy()
    y_test = test["unemployment_rate"].to_numpy()

    ols = LinearRegression()
    ols.fit(X_train, y_train)
    pred_ols = ols.predict(X_test)

    rf = RandomForestRegressor(
        n_estimators=400,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    pred_rf = rf.predict(X_test)

    results = pd.DataFrame(
        {
            "model": ["OLS", "Random Forest"],
            "test_r2": [r2_score(y_test, pred_ols), r2_score(y_test, pred_rf)],
            "test_rmse": [
                np.sqrt(mean_squared_error(y_test, pred_ols)),
                np.sqrt(mean_squared_error(y_test, pred_rf)),
            ],
            "n_train": [len(train), len(train)],
            "n_test": [len(test), len(test)],
            "time_split_cutoff": [cutoff.date(), cutoff.date()],
        }
    )

    return results


def run_diagnostics(fe_result, data: pd.DataFrame, x_cols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run Breusch-Pagan, VIF, and save residual diagnostic plots."""
    residuals = np.asarray(fe_result.resids).reshape(-1)
    fitted = np.asarray(fe_result.fitted_values).reshape(-1)

    X_bp = sm.add_constant(data[x_cols])
    bp_stat, bp_pval, f_stat, f_pval = het_breuschpagan(residuals, X_bp)

    diagnostics = pd.DataFrame(
        {
            "metric": [
                "breusch_pagan_lm_stat",
                "breusch_pagan_lm_pvalue",
                "breusch_pagan_f_stat",
                "breusch_pagan_f_pvalue",
                "residual_mean",
                "residual_std",
            ],
            "value": [bp_stat, bp_pval, f_stat, f_pval, residuals.mean(), residuals.std()],
        }
    )

    vif_df = pd.DataFrame(
        {
            "variable": x_cols,
            "vif": [
                variance_inflation_factor(data[x_cols].to_numpy(), i)
                for i in range(len(x_cols))
            ],
        }
    )

    # Residuals vs fitted
    plt.figure(figsize=(10, 6))
    plt.scatter(fitted, residuals, alpha=0.25)
    plt.axhline(0.0, color="red", linestyle="--", linewidth=1)
    plt.xlabel("Fitted values")
    plt.ylabel("Residuals")
    plt.title("M3 Model A: Residuals vs Fitted")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_residuals_vs_fitted.png", dpi=300)
    plt.close()

    # Q-Q plot
    plt.figure(figsize=(8, 6))
    stats.probplot(residuals, dist="norm", plot=plt)
    plt.title("M3 Model A: Q-Q Plot")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_qq_plot.png", dpi=300)
    plt.close()

    return diagnostics, vif_df


def robustness_checks(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run required robustness checks for Model A."""
    comparison_rows = []

    # 1) Clustered vs unadjusted standard errors
    data_lag2 = prepare_model_data(df, fed_lag=2)
    fe_unadj, _ = fit_fixed_effects(data_lag2, fed_lag=2, clustered=False)
    fe_cluster, _ = fit_fixed_effects(data_lag2, fed_lag=2, clustered=True)
    key_var = "fedfunds_lag2_x_high_unemp"
    comparison_rows.append(
        {
            "check": "clustered_vs_unadjusted_se",
            "spec": "lag2_interaction",
            "coef": fe_cluster.params.get(key_var, np.nan),
            "se_unadjusted": fe_unadj.std_errors.get(key_var, np.nan),
            "se_clustered": fe_cluster.std_errors.get(key_var, np.nan),
            "p_unadjusted": fe_unadj.pvalues.get(key_var, np.nan),
            "p_clustered": fe_cluster.pvalues.get(key_var, np.nan),
            "n_obs": fe_cluster.nobs,
        }
    )

    # 2) Alternative lag structures
    lag_rows = []
    for lag in [0, 1, 2, 3]:
        lag_data = prepare_model_data(df, fed_lag=lag)
        lag_res, _ = fit_fixed_effects(lag_data, fed_lag=lag, clustered=True)
        lag_var = f"fedfunds_lag{lag}_x_high_unemp"
        lag_rows.append(
            {
                "lag": lag,
                "coef": lag_res.params.get(lag_var, np.nan),
                "se_clustered": lag_res.std_errors.get(lag_var, np.nan),
                "p_value": lag_res.pvalues.get(lag_var, np.nan),
                "n_obs": lag_res.nobs,
                "r2_within": lag_res.rsquared_within,
            }
        )

    # 3) Exclude COVID outlier window (Mar-May 2020)
    no_covid = df[
        ~((df["date"] >= "2020-03-01") & (df["date"] <= "2020-05-31"))
    ].copy()
    no_covid_data = prepare_model_data(no_covid, fed_lag=2)
    no_covid_res, _ = fit_fixed_effects(no_covid_data, fed_lag=2, clustered=True)
    comparison_rows.append(
        {
            "check": "exclude_covid_2020_03_to_2020_05",
            "spec": "lag2_interaction",
            "coef": no_covid_res.params.get(key_var, np.nan),
            "se_unadjusted": np.nan,
            "se_clustered": no_covid_res.std_errors.get(key_var, np.nan),
            "p_unadjusted": np.nan,
            "p_clustered": no_covid_res.pvalues.get(key_var, np.nan),
            "n_obs": no_covid_res.nobs,
        }
    )

    return pd.DataFrame(comparison_rows), pd.DataFrame(lag_rows)


def build_publication_table(fe_unadj, fe_cluster, ml_results: pd.DataFrame) -> pd.DataFrame:
    """Build a side-by-side publication-style summary table."""
    rows = []

    var_map = {
        "fedfunds_lag2_x_high_unemp": "Fed Funds (lag2) x High-Unemp State",
        "unemployment_lag1": "Unemployment Lag(1)",
        "recession_x_high_unemp": "Recession x High-Unemp State",
    }

    for var, label in var_map.items():
        coef_1 = fe_unadj.params.get(var, np.nan)
        p_1 = fe_unadj.pvalues.get(var, np.nan)
        se_1 = fe_unadj.std_errors.get(var, np.nan)

        coef_2 = fe_cluster.params.get(var, np.nan)
        p_2 = fe_cluster.pvalues.get(var, np.nan)
        se_2 = fe_cluster.std_errors.get(var, np.nan)

        rows.append(
            {
                "variable": label,
                "model1_fe_unadjusted": f"{coef_1:.4f}{significance_stars(p_1)}",
                "model1_se": f"({se_1:.4f})",
                "model2_fe_clustered": f"{coef_2:.4f}{significance_stars(p_2)}",
                "model2_se": f"({se_2:.4f})",
                "model3_ml": "",
            }
        )

    ols_r2 = ml_results.loc[ml_results["model"] == "OLS", "test_r2"].iloc[0]
    ols_rmse = ml_results.loc[ml_results["model"] == "OLS", "test_rmse"].iloc[0]
    rf_r2 = ml_results.loc[ml_results["model"] == "Random Forest", "test_r2"].iloc[0]
    rf_rmse = ml_results.loc[ml_results["model"] == "Random Forest", "test_rmse"].iloc[0]

    rows += [
        {
            "variable": "Entity FE",
            "model1_fe_unadjusted": "Yes",
            "model1_se": "",
            "model2_fe_clustered": "Yes",
            "model2_se": "",
            "model3_ml": "State one-hot",
        },
        {
            "variable": "Time FE",
            "model1_fe_unadjusted": "Yes",
            "model1_se": "",
            "model2_fe_clustered": "Yes",
            "model2_se": "",
            "model3_ml": "Time split (80/20)",
        },
        {
            "variable": "Clustered SE",
            "model1_fe_unadjusted": "No",
            "model1_se": "",
            "model2_fe_clustered": "Yes (state)",
            "model2_se": "",
            "model3_ml": "N/A",
        },
        {
            "variable": "N",
            "model1_fe_unadjusted": f"{int(fe_unadj.nobs):,}",
            "model1_se": "",
            "model2_fe_clustered": f"{int(fe_cluster.nobs):,}",
            "model2_se": "",
            "model3_ml": f"Train/Test: {int(ml_results['n_train'].iloc[0]):,}/{int(ml_results['n_test'].iloc[0]):,}",
        },
        {
            "variable": "R2 (within)",
            "model1_fe_unadjusted": f"{fe_unadj.rsquared_within:.4f}",
            "model1_se": "",
            "model2_fe_clustered": f"{fe_cluster.rsquared_within:.4f}",
            "model2_se": "",
            "model3_ml": f"OLS R2={ols_r2:.4f}; RF R2={rf_r2:.4f}",
        },
        {
            "variable": "RMSE (test)",
            "model1_fe_unadjusted": "N/A",
            "model1_se": "",
            "model2_fe_clustered": "N/A",
            "model2_se": "",
            "model3_ml": f"OLS={ols_rmse:.4f}; RF={rf_rmse:.4f}",
        },
        {
            "variable": "Notes",
            "model1_fe_unadjusted": "SE in parentheses",
            "model1_se": "",
            "model2_fe_clustered": "*** p<0.01, ** p<0.05, * p<0.10",
            "model2_se": "",
            "model3_ml": "Out-of-sample evaluation",
        },
    ]

    return pd.DataFrame(rows)


def main() -> None:
    print("=" * 72)
    print("Milestone 3 Econometric Models")
    print("=" * 72)

    df = load_data()
    df = build_features(df)

    # Model A (required): two-way fixed effects
    model_data = prepare_model_data(df, fed_lag=2)
    fe_unadj, x_cols = fit_fixed_effects(model_data, fed_lag=2, clustered=False)
    fe_cluster, _ = fit_fixed_effects(model_data, fed_lag=2, clustered=True)

    # Model B (option 3): ML comparison
    ml_results = model_b_ml_comparison(df)

    # Diagnostics and robustness
    diagnostics, vif_table = run_diagnostics(fe_cluster, model_data, x_cols)
    robust_table, lag_table = robustness_checks(df)

    # Publication outputs
    regression_table = build_publication_table(fe_unadj, fe_cluster, ml_results)

    regression_table.to_csv(TABLES_DIR / "M3_regression_table.csv", index=False)
    diagnostics.to_csv(TABLES_DIR / "M3_diagnostics_summary.csv", index=False)
    vif_table.to_csv(TABLES_DIR / "M3_vif_table.csv", index=False)
    robust_table.to_csv(TABLES_DIR / "M3_robustness_summary.csv", index=False)
    lag_table.to_csv(TABLES_DIR / "M3_robustness_lag_table.csv", index=False)
    ml_results.to_csv(TABLES_DIR / "M3_model_b_ml_comparison.csv", index=False)

    # Save text summaries for reproducible audit trail
    with open(TABLES_DIR / "M3_modelA_fe_unadjusted_summary.txt", "w", encoding="utf-8") as f:
        f.write(str(fe_unadj.summary))

    with open(TABLES_DIR / "M3_modelA_fe_clustered_summary.txt", "w", encoding="utf-8") as f:
        f.write(str(fe_cluster.summary))

    # Optional quick figure to accompany Model B comparison
    plt.figure(figsize=(7, 5))
    plot_df = ml_results.melt(id_vars="model", value_vars=["test_r2", "test_rmse"])
    sns.barplot(data=plot_df, x="variable", y="value", hue="model")
    plt.title("M3 Model B: OLS vs Random Forest")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "M3_model_b_performance.png", dpi=300)
    plt.close()

    print("Saved tables:")
    print(f"- {TABLES_DIR / 'M3_regression_table.csv'}")
    print(f"- {TABLES_DIR / 'M3_diagnostics_summary.csv'}")
    print(f"- {TABLES_DIR / 'M3_vif_table.csv'}")
    print(f"- {TABLES_DIR / 'M3_robustness_summary.csv'}")
    print(f"- {TABLES_DIR / 'M3_robustness_lag_table.csv'}")
    print(f"- {TABLES_DIR / 'M3_model_b_ml_comparison.csv'}")
    print("Saved figures:")
    print(f"- {FIGURES_DIR / 'M3_residuals_vs_fitted.png'}")
    print(f"- {FIGURES_DIR / 'M3_qq_plot.png'}")
    print(f"- {FIGURES_DIR / 'M3_model_b_performance.png'}")


if __name__ == "__main__":
    main()
