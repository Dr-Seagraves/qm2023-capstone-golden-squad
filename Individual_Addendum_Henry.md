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
| **M1: [Data pipeline]** | [2] hrs | [Data extraction/quailty control] | [Specific outputs: Data Quality Report and process data, importing data] |
| **M2: [EDA]** | [1.5] hrs | [quilty control analyst/ feedback advisor/report verificiation] | [Specific outputs: EDA reports/figures] |
| **M3: [Econometric model]** | [1] hrs | [execution management/feedback specialist] | [Specific outputs: Econometric models and interpretations] |
| **M4: Policy/Investment Memo** | [1.5] hrs | [Presenation Designer/data management/feedback] | [Specific sections: Investment memo, presentation, and individual addendum] |
| **TOTAL** | **[6] hrs** | [I had a wide variety of roles on the project. I processed data as well as fixed up models, making sure they are not just doing what they are preciving, but what we actually want. I designed the presentation, importing models and stats we thought are key to the project.] |

**Team Contribution:** [6]/[22] = [27]% of team workload

--- 

## 2. One Defended Methodological Decision

**Decision Made:** [Exclusion of the District of Columbia, Hawaii to maintain a panel of 48 states ]

**Thesis:** [Adding data from the district of Columbia and the upper states would introduce many significant statistical outliers and skew results, due to the difference in geography, socioeconomic, and administrative tendencencys the data was left out. ]

**Evidence:**

*Empirical Support:*
- [Outlier Influence, We found District of Columbia was far outside of the mean so it made no sense to add it. ]
- [Sensitivity Analysis, We found DC was highly sensitive to changes in economic policy compared to other states.]
- [Quantitative Evidence: In the 48-state model, we achieved a p-value = 0.032. When D.C. was included in exploratory runs, the p-value rose to 0.15, rendering the core policy finding statistically insignificant]

**Alternative Specifications Considered:**

1. **[Inclusion of D.C. with Dummy Variables]:** [Rejected]
   - Weakness: [Even with the dummy varibles it still did not account for the diffrence in the employment levels due to change in economic policy ]
   - Reason: [It added unessecary complexity to the project that was not needed. ]

2. **[Inclusion of Alaska and Hawaii]:** [Rejected]
   - Weakness: [Higher costs of living as well as supply chain diffrences did not meet our goal of consistency.]
   - Reason: [To maintain a continous geographic focus, that allowed us to see the actual effects of economic policy change. ]

**Bottom Line:** Your choice yields [a stable and statistically significant coefficient] and is defensible for [policy-oriented decision-making]

---

## 3. One Key Limitation & Mitigation Strategy

**Limitation:** [Fixed Effects Time-Invariance Assumption]

**Why This Matters:**

- **Core concern:** [The model assumes that diffrences from state to state do not change or evolve. It assumes they are constant. If employment volitility follows diffrent trends from state to state this could lead to huge differences in the in actual results. ]
- **Potential bias:** [If high-unemployment states were already improving or declining, this would be considered a change due to monetary policy.]
- **Real example:** [States with a reliance on heavy manufacturing, could be seen as losing jobs due to monetary policy. However it is just a real change in the economy and the way its changing for manufacturing jobs.]

**Specific Mitigation Tests (Future Work):**

1. **[State Specific Trends]:** [Add nessecary information for state specific info, allowing people to see how a states employment is changing over time, aside from unemployment.]
2. **[Sub-sample splits]:** [Run the model for specific time periods within the data set to see if the relationship stays the same after economic shocks.]  
3. **[Placebo test]:** [Test with intrest rates to see if economic policy is actually driving employment.]

**Severity Assessment:** [Medium]
- Reasoning: [While fixed effects can account for permenet state diffrences, 35 years is a long time for an economy to remain the same. But having the amount of data we have and the national time fixed effects, we mitigate this risk for short term findings. ]

---

## 4. Self-Reflection: Strengths, Growth Areas & Key Learnings

**What I Did Particularly Well:**

I did an excellent job with data assesment, I feel I was able to interpret the output of the model. I was able to identify errors and irradicate them as they occured. These adjustments were critical to the accuracy of our project. 

---

**What I Could Have Improved:**

I could have spent more time actually auditing the output of the AI. I put a lot of trust on the ability of the Ai to execute the task. 
---

**Key Learning from This Capstone:**

[I learned teamwork skills regarding AI usage/augmentation. I also learned how to more effectivly prompt the AI. During Milestone three I ran into some errors, with some cleaver prompting I was able to clean them right up. Proper prompting is somthing I will carry forward with me as I continue to develope and use AI skills and platforms.  ]

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
