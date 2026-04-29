# Individual Contribution Statement [TEMPLATE]
## QM 2023 Capstone Project - Milestone 4

---

**Name:** [Rylan Leathers]
**Team:** [Golden Squad]  
**Date:** [May 1st]

---

## 1. Contribution Summary

| Milestone | Hours | Role(s) | Key Deliverables |
|-----------|-------|---------|------------------|
| **M1: [Data pipeline]** | [2] hrs | [Data extraction/quailty control] | [Specific outputs: Data Quality Report and process data] |
| **M2: [EDA]** | [1.5] hrs | [quilty control analyst/ feedback specilaist] | [Specific outputs: EDA reports/figures] |
| **M3: [Econometric model]** | [1.5] hrs | [execution management/feedback specialist] | [Specific outputs: Econometric models and interpretations] |
| **M4: Policy/Investment Memo** | [1] hrs | [execution management/feedback specialist] | [Specific sections: Investment meno, presentation, and individual addendum] |
| **TOTAL** | **[6] hrs** | [quility control/feedback specialist/Data extraction] | [Helped to look over/maintain and give feedback to out team over the new code the ai helped write while also pulling data to give to the AI.  ] |

**Team Contribution:** [6]/[22] = [27]% of team workload

--- 

## 2. One Defended Methodological Decision

**Decision Made:** [i used number of langs in the model and cluster at the state level.]

**Thesis:** [We use a lag structure chosen by the Bayesian Information Criterion to balance capturing dynamics with avoiding overfitting. The results show a consistent, statistically significant negative effect (about −0.3 to −0.5) across nearby lag choices.]

**Evidence:**

*Empirical Support:*
- [indicating a statistically significant negative effect.]
- [n M3, using 3 lags yields coef and 5 lags give -.45 which is showing magnitude and direction]
- [Preferred model p-value = 0.01 vs. p = 0.12 in a misspecified 1-lag model, suggesting improved fit and inference.]

*Economic Theory:*
- [Theoretical foundation: Prior work in Econometrics and Time Series Analysis supports including multiple lags to capture delayed adjustment effects.]
- [Mechanism: The effect operates with delay because changes in the explanatory variable take time to transmit through economic or behavioral channels.]
- [Consistency: The negative relationship remains stable across alternative lag lengths and subsamples, supporting a persistent underlying effect.]

**Alternative Specifications Considered:**

1. **[Fewer lag specification]:** [Why you rejected it]
   - Weakness: [Statistically weaker results (e.g., p-value ≈ 0.15–0.20) and evidence of residual autocorrelation, suggesting model misspecification.]
   - Reason: [Theoretically inconsistent with the literature in Econometrics and Time Series Analysis, which supports delayed adjustment effects rather than immediate responses.]

2. **[Excessive lag specification]:** [Why you rejected it]
   - Weakness: [Increased noise and instability in coefficients, with wider standard errors and reduced statistical significance.]
   - Reason: [Overfitting concern—additional lags capture short-term noise rather than meaningful dynamics, making interpretation less reliable.]

**Bottom Line:** our preferred specification yields a stable negative effect (approximately −0.3 to −0.5) and is defensible for causal interpretation and policy-relevant inference due to its balance between model fit and dynamic structure.

---

## 3. One Key Limitation & Mitigation Strategy

**Limitation:** [Lag selection sensitivity]

**Why This Matters:** 

- **Core concern:** [small changes in the number of lags lead to big changes in your results]
- **Potential bias:** [potential bias in your estimates and conclusions and it can creep in from multiple directions depending on how you choose the lag length.]
- **Real example:** [Suppose you’re studying whether changes in interest rates affect inflation using a time-series model]

**Specific Mitigation Tests (Future Work):**

1. **[test 1]:** [Lag robustness sweep]
2. **[Test 2]:** [Structural stability / split-sample test]  
3. **[Test 3]:** [Residual diagnostics and autocorrelation check]

**Severity Assessment:** [Low/Medium/High]
- Reasoning: [Medium severity. AI helped fix our errors that we descovered while also showing and telling us why.]

---

## 4. Self-Reflection: Strengths, Growth Areas & Key Learnings

**What I Did Particularly Well:**

[I did well at looking back through the assignment as well as asking the AI for help.]



**What I Could Have Improved:**

[I could have improved on the diffenet task i was asking the AI and how i could have made it more clear. ]



**Key Learning from This Capstone:**

[I learned teamwork skills regarding AI usage is very helpful and important when working with something of this size. I aslo learned that being able to work with this powerful AI has completly opend my eyes to everything that is capable with AI. ]



---

## 5. AI Tool Usage & Verification


**Estimated AI Assistance:** [95]% of [all] coding / [80]% of [all] writing


See AI audit 

---

## 6. Attestation

I affirm that:
- All contributions listed above are accurate and honest
- I have not exaggerated my role or minimized teammates' contributions  
- I understand this addendum may be used to adjust my individual grade
- I take responsibility for my work

**Signature:** ____rylan Leathers________________  
**Date:** ______04-29-2026____________

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
