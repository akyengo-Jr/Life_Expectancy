## Notebook Documentation: Exploratory Data Analysis (EDA)

This notebook performs a comprehensive exploratory data analysis (EDA) on the cleaned Life Expectancy dataset. The following steps and analyses have been conducted:

1. **Data Loading and Overview**
   - Loaded the cleaned dataset and displayed the first few rows.
   - Inspected data types, column names, and basic statistics.

2. **Missing Value Analysis**
   - Checked for missing values in each column to confirm data cleanliness.

3. **Target Variable Exploration**
   - Visualized the distribution of the target variable (`Life expectancy`).

4. **Feature Correlation**
   - Generated a correlation heatmap for all numeric features to identify relationships and multicollinearity.

5. **Univariate Feature Distributions**
   - Plotted histograms for key features such as GDP, Schooling, BMI, and Adult Mortality.

6. **Country Status Analysis**
   - Analyzed and visualized the distribution of countries by development status (Developed vs Developing).

7. **Bivariate Relationships**
   - Created scatter plots to explore relationships between `Life expectancy` and key features.
   - Visualized `Life expectancy` vs GDP by country status.
   - Used pairplots to examine pairwise relationships among important variables.

8. **Temporal Trends**
   - Plotted life expectancy trends over time, segmented by country status.

9. **Outlier and Distribution Analysis**
   - Used boxplots to inspect the distribution and outliers in numerical variables.

10. **EDA Insights for Modeling**
    - Summarized key findings, including skewed features, important predictors, and potential feature interactions for the modeling phase.

---
This documentation provides a clear overview of the EDA process and the insights gained to inform subsequent modeling steps.