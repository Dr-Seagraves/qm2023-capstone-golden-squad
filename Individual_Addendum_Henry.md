# Individual Contribution Statement
## QM 2023 Capstone Project - Milestone 4

---

**Name:** [Henry Simon]
**Team:** [Golden Squad]  
**Date:** [May 1st]

---

## 1. Contribution Summary

| Milestone | Hours | Role(s) | Key Deliverables |
|-----------|-------|---------|------------------|
| **M1: [Data pipeline]** | [2] hrs | [Data extraction/quality control] | [Specific outputs: Data Quality Report and process data, importing data] |
| **M2: [EDA]** | [1.5] hrs | [quality control analyst/ feedback advisor/report verification] | [Specific outputs: EDA reports/figures] |
| **M3: [Econometric model]** | [1] hrs | [execution management/feedback specialist] | [Specific outputs: Econometric models and interpretations] |
| **M4: Policy/Investment Memo** | [1.5] hrs | [Presentation Designer/data management/feedback] | [Specific sections: Investment memo, presentation, and individual addendum] |
| **TOTAL** | **[6] hrs** | [I had a wide variety of roles on the project. I processed data as well as fixed up models, making sure they are not just doing what they are perceiving, but what we actually want. I designed the presentation, incorporating models and stats we thought are key to the project.] |

**Team Contribution:** [6]/[22] = [27]% of team workload

--- 

## 2. One Defended Methodological Decision

**Decision Made:** [Exclusion of the District of Columbia, Hawaii, and Alaska to maintain a panel of 48 states ]

**Thesis:** [Adding data from the District of Columbia and the upper states would introduce many significant statistical outliers and skew results due to differences in geography, socioeconomic, and administrative tendencies, so the data was left out. ]

**Evidence:**

*Empirical Support:*
- [Outlier Influence, We found the District of Columbia was far outside the mean, so it made no sense to add it. ]
- [Sensitivity Analysis, We found DC was highly sensitive to changes in economic policy compared to other states.]
- [Quantitative Evidence: In the 48-state model, we achieved a p-value = 0.032. When D.C. was included in exploratory runs, the p-value rose to 0.15, rendering the core policy finding statistically insignificant]

**Alternative Specifications Considered:**

1. **[Inclusion of D.C. with Dummy Variables]:** [Rejected]
   - Weakness: [Even with the dummy variables, it still did not account for the difference in employment levels due to changes in economic policy. ]
   - Reason: [It added unnecessary complexity to the project that was not needed. ]

2. **[Inclusion of Alaska and Hawaii]:** [Rejected]
   - Weakness: [Higher costs of living as well as supply chain differences did not meet our goal of consistency.]
   - Reason: [To maintain a continuous geographic focus that allowed us to see the actual effects of economic policy change. ]

**Bottom Line:** Your choice yields [a stable and statistically significant coefficient] and is defensible for [policy-oriented decision-making]

---

## 3. One Key Limitation & Mitigation Strategy

**Limitation:** [Fixed Effects Time-Invariance Assumption]

**Why This Matters:**

- **Core concern:** [The model assumes that differences from state to state do not change or evolve. It assumes they are constant. If employment volatility follows different trends from state to state, this could lead to huge differences in the actual results. ]
- **Potential bias:** [If high-unemployment states were already improving or declining, this would be considered a change due to monetary policy.]
- **Real example:** [States with a reliance on heavy manufacturing could be seen as losing jobs due to monetary policy. However, it may just be a real change in the economy and the way it is changing for manufacturing jobs.]

**Specific Mitigation Tests (Future Work):**

1. **[State Specific Trends]:** [Add necessary information for state-specific information, allowing people to see how a state's employment is changing over time, aside from unemployment.]
2. **[Sub-sample splits]:** [Run the model for specific time periods within the data set to see if the relationship stays the same after economic shocks.]  
3. **[Placebo test]:** [Test with interest rates to see if economic policy is actually driving employment.]

**Severity Assessment:** [Medium]
- Reasoning: [While fixed effects can account for permanent state differences, 35 years is a long time for an economy to remain the same. With the amount of data we have and the national time fixed effects, we mitigate this risk for short-term findings. ]

---

## 4. Self-Reflection: Strengths, Growth Areas & Key Learnings

**What I Did Particularly Well:**

I did an excellent job with data assessment. I feel I was able to interpret the output of the model. I was able to identify errors and eradicate them as they occurred. These adjustments were critical to the accuracy of our project. 

---

**What I Could Have Improved:**

I could have spent more time actually auditing the output of the AI. I put a lot of trust in the ability of the AI to execute the task. 
---

**Key Learning from This Capstone:**

[I learned teamwork skills regarding AI usage/augmentation. I also learned how to more effectively prompt the AI. During Milestone Three I ran into some errors; with some clever prompting I was able to clean them right up. Proper prompting is something I will carry forward with me as I continue to develop and use AI skills and platforms.  ]

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

**Signature:** ____Henry Simon________________  
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
