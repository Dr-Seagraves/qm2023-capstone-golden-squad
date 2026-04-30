# Individual Contribution Statement [TEMPLATE]
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
| **M2: [EDA]** | [1.5] hrs | [quilty control analyst/ feedback specilaist] | [Specific outputs: EDA reports/figures] |
| **M3: [Econometric model]** | [1] hrs | [execution management/feedback specialist] | [Specific outputs: Econometric models and interpretations] |
| **M4: Policy/Investment Memo** | [1.5] hrs | [Presenation Designer/data management/feedback] | [Specific sections: Investment memo, presentation, and individual addendum] |
| **TOTAL** | **[6] hrs** | [I had a wide variety of roles on the project. I processed data as well as fixed up models, making sure they are not just doing what they are preciving, but what we actually want. I designed the presentation, importing models and stats we thought are key to the project.] |

**Team Contribution:** [6]/[22] = [27]% of team workload

--- 

## 2. One Defended Methodological Decision

**Decision Made:** [State your specific methodological choice clearly]

**Thesis:** [1-2 sentence justification for why this choice is sound]

**Evidence:**

*Empirical Support:*
- [M2/M3 data finding, e.g., "Lag analysis showed strongest correlation at X-month lag"]
- [Robustness result, e.g., "Coefficient stable across alternative specifications"]
- [Quantitative evidence, e.g., "p-value = 0.032, compared to p = 0.15 for alternative"]

*Economic Theory:*
- [Theoretical foundation, e.g., "Literature supports X-month transmission lag"]
- [Mechanism, e.g., "Because [explanation of causal channel]"]
- [Consistency, e.g., "Result robust across different subgroups/time periods"]

**Alternative Specifications Considered:**

1. **[Alternative 1]:** [Why you rejected it]
   - Weakness: [e.g., "Statistically weaker; p-value = 0.20"]
   - Reason: [e.g., "Theoretically inconsistent with literature"]

2. **[Alternative 2]:** [Why you rejected it]
   - Weakness: [specific limitation]
   - Reason: [theoretical or practical objection]

**Bottom Line:** Your choice yields [KEY COEFFICIENT/RESULT] and is defensible for [decision-making context]

---

## 3. One Key Limitation & Mitigation Strategy

**Limitation:** [Fixed Effects Time-Invariance Assumption]

**Why This Matters:**

- **Core concern:** [The model assumes that diffrences from state to state do not change or evolve. It assumes they are constant. If employment volitility follows diffrent trends from state to state this could lead to huge differences in the in actual results. ]
- **Potential bias:** [If high-unemployment states were already improving or declining, this would be considered a change due to monetary policy.]
- **Real example:** [States with a reliance on heavy manufacturing, could be seen as losing jobs due to monetary policy. However it is just a real change in the economy and the way its changing for manufacturing jobs.]

**Specific Mitigation Tests (Future Work):**

1. **[Test 1]:** [What robustness check would help - e.g., "Include time-varying state controls and reestimate"]
2. **[Test 2]:** [Alternative validation - e.g., "Split sample pre/post structural break"]  
3. **[Test 3]:** [Specification check - e.g., "Use placebo variables to test for omitted bias"]

**Severity Assessment:** [Low/Medium/High]
- Reasoning: [1-2 sentences on whether this substantially undermines findings]

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
