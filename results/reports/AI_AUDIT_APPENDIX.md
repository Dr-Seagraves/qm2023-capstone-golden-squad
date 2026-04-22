# AI Audit Appendix Capstone M1

## Tool(s) Used
- GitHub Copilot

## Task(s) Where AI Was Used
- To help code the fetch of data, cleaning of data, and merging of data. Also was used to help update documents, instructions, etc. Helped in maintaining reproducability as well as organization and overall understanding and structure of milestone. 

## Prompt(s)
- See AI_Chat_Logs Folder

## Output Summary
- See AI_Chat_Logs Folder

## Verification & Modifications (Disclose • Verify • Critique)
- **Verify:** Ran the script and made sure all documents, data, etc followed the M1 guidelines provided
- **Critique:** Not much as of now, had some errors in the organization and structure of the milestone which was then required to be done manually in some regards. It also had issues downloading data at times, forcing us to use BLS data in addition to FRED data.
- **Modify:** A full folder of code, data, etc was provided thanks to the GitHub copilot.

## If No AI Tools Used
Write: "No AI tools were used for this assignment."\



# AI Audit Appendix Capstone M2

## Tool(s) Used
- GitHub Copilot

## Task(s) Where AI Was Used
- To help code the juipter notebook and update the README file according to the updates done in M2. Also helped summarize all outputs as showin in the M2 EDA Summary.

## Prompt(s)
- See AI_Chat_Logs Folder

## Output Summary
- See AI_Chat_Logs Folder

## Verification & Modifications (Disclose • Verify • Critique)
- **Verify:** Ran the script and made sure all documents, data, etc followed the M2 guidelines provided. Also made sure that the EDA graphs/figures given followed some line of reasoning/economic theory.
- **Critique:** Not much as of now, had some minor documentation issues and adding of unecessary files that then needed to be cleaned/reorganized later. Also had to do quite a bit of guidance at times/multiple prompts, which is common with AI nowadays, rarely does an AI complete a project perfectly with one prompt.
- **Modify:** A full EDA notebook and subsequently the figures from the notebook were provided thanks to the GitHub copilot, saving us significant amount of time. 

## If No AI Tools Used
Write: "No AI tools were used for this assignment."



# AI Audit Appendix Capstone M3

## Tool(s) Used
- GitHub Copilot

## Task(s) Where AI Was Used
- To draft and iterate on `code/capstone_models.py` (Model A FE + Model B ML comparison).
- To structure required diagnostics (Breusch-Pagan, VIF, residual plots).
- To design and implement robustness checks (clustered vs unadjusted SE, lag sensitivity, excluding COVID outliers).
- To format publication-style output tables and produce memo-ready interpretation content.

## Prompt(s)
- Full interaction logs are in `AI_Chat_Logs/M3/4_20 2PM`.
- Representative M3 prompts used:
	- "Implement an M3 pipeline that runs two-way FE and a secondary model comparison, saving tables/figures to results folders."
	- "Add required diagnostics: heteroskedasticity test, VIF, and residual diagnostic plots."
	- "Add at least three robustness checks and output publication-ready CSV summaries."
	- "Draft interpretation language for coefficients, robustness, caveats, and model comparison."

## Output Summary
- AI generated and refined code sections in `code/capstone_models.py`.
- AI-assisted outputs created in:
	- `results/tables/M3_regression_table.csv`
	- `results/tables/M3_diagnostics_summary.csv`
	- `results/tables/M3_vif_table.csv`
	- `results/tables/M3_robustness_summary.csv`
	- `results/tables/M3_robustness_lag_table.csv`
	- `results/tables/M3_model_b_ml_comparison.csv`
	- `results/figures/M3_residuals_vs_fitted.png`
	- `results/figures/M3_qq_plot.png`
	- `results/figures/M3_model_b_performance.png`
- AI-assisted interpretation draft contributed to `M3_interpretation.md`.

## Verification & Modifications (Disclose • Verify • Critique)
- **Verify:** Re-ran the model script and checked that required files were written to `results/tables/` and `results/figures/`; confirmed key diagnostics and robustness outputs were present and non-empty.
- **Verify:** Checked that Model A used entity and time fixed effects with clustered SEs and that Model B comparison reported out-of-sample metrics (R2 and RMSE).
- **Critique:** Initial AI drafts required clarification on folder naming and output placement; some interpretations were tightened to use percentage-point language and to separate statistical significance from economic interpretation.
- **Modify:** We edited wording and organization in the interpretation memo, kept only relevant outputs, and aligned file names/paths with rubric and README expectations.

## If No AI Tools Used
Write: "No AI tools were used for this assignment."