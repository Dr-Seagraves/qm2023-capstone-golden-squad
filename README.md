[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22639587&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Project Structure

- **code/** — Python scripts and notebooks. Use `config_paths.py` for paths.
    Fetch data scripts, merge scripts.
- **data/raw/** — Original data (read-only)
    Unemployment rates from all 50 states as well as the national federal funds rate over time.
- **data/processed/** — Intermediate cleaning outputs
- **data/final/** — M1 output: analysis-ready panel
- **results/figures/** — Visualizations
- **results/tables/** — Regression tables, summary stats
- **results/reports/** — Milestone memos
- **tests/** — Autograding test suite

Run `python code/config_paths.py` to verify paths.

2/20 Update

Research Question: How do interest rates/federal fund rates affect unemployment rates across the United States over time?

Project Idea: We will be analyzing the national federal fund rates and compare that to unemployment rate data across all US states to see if there is any correlation. While the 2 aren't directly linked, we know that interest rates can affect investment, consumer spending, borrowing costs, etc. which in turn can have an effect on unemployment rates.
