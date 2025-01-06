# README: Epilepsy Surgery Outcome Analysis

## Project Overview
This project investigates the relationship between the age of epilepsy onset and the success of epilepsy surgery. By analyzing a dataset of patients who underwent epilepsy surgery, we aim to identify how age at onset affects surgical outcomes over five years post-surgery.

## Dataset
- **Source:** Provided dataset named `Metadata_Release_Anon.csv`.
- **Participants:** 443 individuals who underwent epilepsy surgery.
- **Key Features:**
  - Demographic information (e.g., age at onset, age at surgery).
  - Surgical details (e.g., type of surgery, pathology).
  - Outcome metrics (e.g., seizure freedom scores, ILAE classification).

## Research Question
Does the age of epilepsy onset influence the success rate of epilepsy surgery?

## Methodology
1. **Data Preparation:**
   - Defined surgical success as achieving an ILAE score ≤ 2 (freedom or near freedom from seizures).
   - Grouped participants by binned onset age (e.g., "1 to 2", "5 to 7").
   - Calculated success rates for five years post-surgery.

2. **Analysis:**
   - Calculated success rates by year and by age group.
   - Computed average time to reach success by age group.
   - Performed statistical tests (ANOVA and Tukey HSD) to evaluate differences among groups.

3. **Visualization:**
   - Generated visualizations to illustrate:
     - Success rates over time.
     - Average time to success by age group.
     - Trends in success rates comparing children (≤ 15 years) and adults (> 15 years).

## Results
### Key Findings
1. **Success Rates by Year and Age Group:**
   - Success rates varied across age groups and years.
   - Trends indicated higher success rates in certain younger age groups.

2. **Time to Success:**
   - Average time to success differed among age groups, with younger participants often achieving success earlier.

3. **Statistical Analysis:**
   - **ANOVA:** Significant differences found among age groups in Year 2 (p-value = 0.0254), but not in other years.
   - **Post-Hoc Test (Tukey HSD):** No significant pairwise differences identified in Year 2.

## Visualizations
### Included Graphs
1. **Overview of Dataset and Research Question:**
   - Visual summary of project scope and dataset details.

2. **Average Time to Success by Age of Onset:**
   - Bar chart showing the average time to achieve success for each binned age group.

3. **Success Rates by Year and Age Group:**
   - Scatterplots for each year (Years 1 to 5), displaying success rates by binned onset age.

4. **Trends Over Time by Age Group:**
   - Line graph showing success rate trends over five years for each binned age group.

5. **Children vs. Adults:**
   - Side-by-side line graphs comparing success trends over five years for children (≤ 15 years) and adults (> 15 years).

6. **Tukey HSD Results:**
   - Table and graph summarizing pairwise comparisons of age groups for Year 2.

## File Structure
- `analysis_code.py`: Python script for data processing, statistical analysis, and visualization.
- `Metadata_Release_Anon.csv`: Dataset used for analysis.
- `success_rates_by_year.csv`: Processed data showing success rates by year.
- `avg_time_to_success.csv`: Average time to success by age group.

## How to Run the Analysis
1. Clone this repository.
2. Install required Python libraries:
   ```bash
   pip install pandas numpy matplotlib statsmodels scipy
   ```
3. Run the analysis script:
   ```bash
   python analysis_code.py
   ```
4. Output visualizations and processed data will be saved in the working directory.

## Limitations
1. **Small Sample Sizes**:
   - Certain age groups, such as `< 1` and `40 to 44`, had very few participants, which limits generalizability.
2. **Missing Data**:
   - Missing values in later years (`ILAE_Year5`) reduced the dataset for long-term analysis.
3. **Intra-Group Variability**:
   - Differences in surgical types and pathologies within age groups could obscure trends.
4. **Uniform Definition of Success**:
   - Success was uniformly defined as `ILAE <= 2`, which may not capture nuances in different patient populations.
5. **Limited Timeframe**:
   - The analysis is restricted to five years post-surgery. Longer-term outcomes may show different trends.


## Conclusion
The analysis suggests that the age of epilepsy onset has some influence on surgical success, with differences observed primarily in the second year post-surgery. However, further investigation with additional factors (e.g., type of surgery, pathology) is recommended to confirm and refine these findings.

## Contact
For any questions or suggestions, please contact:
[Your Name]
Email: [Your Email Address]

