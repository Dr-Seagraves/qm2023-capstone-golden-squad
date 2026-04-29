# Individual Contribution Statement
## QM 2023 Capstone Project - Milestone 4

---

**Name:** Trenton Diveley

**Team:** Golden Squad

**Date:** 5/1/2026

---

## 1. Contribution Summary

| Milestone | Hours | Role(s) | Key Deliverables |
|-----------|-------|---------|------------------|
| **M1: Data Pipeline** | 4 hrs | Lead Data Analyst | Specific outputs: Data Quality Report and Processed Data |
| **M2: EDA** | 3 hrs | Lead Data Analyst | Specific outputs: EDA Reports/Figures|
| **M3: Econometric Models** | 2 hrs | Lead Data Analyst | Specific outputs: Econometric Models and Interpretations|
| **M4: Policy/Investment Memo** | 1 hrs | Lead Data Analyst | Specific sections: Investment Memo, Presentation, and Individual Addendum. |
| **TOTAL** | **11 hrs** | Lead Analyst throughout M1-M4 | Overall AI Prompter, organizer, and analyst. Consulted my quality control and feedback specialists for guidance and AI checking. |

**Team Contribution:** 10/22 = 46% of team workload

---

## 2. One Defended Methodological Decision

**Decision Made:** Using a 2 Way FE Model

**Thesis:** This approach is appropriate as it isolates differences across states while still controlling for national shocks, allowing us to identify heterogeneous policy effects that would otherwise be unobservable.

**Evidence:**

*Empirical Support:*
- Lag analysis shows consistent negative effects across 0–3 months (all p < 0.025).
- Main coefficient is statistically significant (p = 0.032) and stable across specifications.
- Results hold with clustered standard errors and high explanatory power (R² ≈ 0.90).

*Economic Theory:*
- Monetary policy affects regions differently based on labor market conditions
- High-Unemployment states are more sensitive dur to cyclical industries and credit constraints.
- Results are consistent across lags, matching expected policy transmission timing

**Alternative Specifications Considered:**

1. **Aggregate Effect Only:** 
   - Weakness: Effect absorbed by FE
   - Reason: Doesn't capture regional differences, which is a core piece

2. **Machine Learning Model:** 
   - Weakness: Slightly worse test performance
   - Reason: Less interpretable and doesn't provide clear coefficients.

**Bottom Line:** My choice yields a -0.0042 differential effect and is defensible for regional heterogeneity and decision making.

---

## 3. One Key Limitation & Mitigation Strategy

**Limitation:** Parallel Trends/Policy Response

**Why This Matters:**

- **Core concern:** This model assumes that high and low unemployment states respond the same witout policy changes. This wouldn't hold because the Fed changes interest rates in response to the economy.
- **Potential bias:** This could overstate the effect in high unemployment states if they were improving.
- **Real example:** Some high unemployment states were already recovering after COVID. If rates increased during that recovery, the model might wrongly credit the rate hike for the improvement.

**Specific Mitigation Tests (Future Work):**

1. **[Test 1]:** Event Study/Pre Trend Check: See if trends were different before policy changes.
2. **[Test 2]:** Add State Controls: Include changing state factors
3. **[Test 3]:** Placebo Test: Utilize fake policy timing to see if results remain

**Severity Assessment:** Medium
- Reasoning: This can matter for causality. If trends weren't parallel, the results may reflect existing differences, not necessarily the true effect of the policy.

---

## 4. Self-Reflection: Strengths, Growth Areas & Key Learnings

**What I Did Particularly Well:**

I did well with taking my time with the GitHub Copilot and documenting prompts, outputs, etc. I also helped organize the structure of the project to make it overall more presentable.

---

**What I Could Have Improved:**

I could've improved on understanding the data/project more as I went through rather than just plugging away to knock out the milestones. I also could've consulted my partners more during each Milestone to help get more feedback earlier on before deadlines.

---

**Key Learning from This Capstone:**

AI Usage and prompting needs to be specific, documented, and monitored. Working as a team requires dignificant amount of communication. GitHub is incredible once you fully understand it capabilities and structure.

---

## 5. AI Tool Usage & Verification


**Estimated AI Assistance:** 95% of all coding / 80% of all writing

See AI Audit Appendix For Addional Information.

---

## 6. Attestation

I affirm that:
- All contributions listed above are accurate and honest
- I have not exaggerated my role or minimized teammates' contributions  
- I understand this addendum may be used to adjust my individual grade
- I take responsibility for my work

**Signature:** Trenton Diveley  
**Date:** 5/1/2026

---

## Submission Guidelines

**Format:** 
- Save as PDF: `Individual_Addendum_[YourLastName].pdf`
- Aim for 1 page (strict limit); use 11-12 pt font, 1-inch margins

**Submission:**
```bash
git add Individual_Addendum_[YourName].pdf
git commit -m "Add individual addendum - [Your Name]"
git push origin main
```

**Deadline:** Friday, Week 14 (May 1) by 11:59 PM
