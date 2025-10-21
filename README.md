# Life Expectancy Prediction using Linear Regression

This project demonstrates how to predict life expectancy using multivariate linear regression, both from scratch and with scikit-learn, on the "Life Expectancy Data.csv" dataset. The notebook includes exploratory data analysis (EDA), model implementation, evaluation, and a discussion of the business value.

---

## Project Overview

- **Goal:** Predict the `Life expectancy` of a country based on various health, demographic, and socio-economic features.
- **Approach:** 
  - Implement linear regression from scratch using gradient descent.
  - Compare results with scikit-learn’s `LinearRegression`.
  - Perform EDA to understand the data and feature relationships.
  - Visualize results and compare model performance.

---

## Contents

- **life_expectancy.ipynb**: Main notebook with all code, EDA, modeling, and visualizations.
- **Life Expectancy Data.csv**: Dataset (not included; please provide your own copy).

---

## How to Run

1. Place `Life Expectancy Data.csv` in the project directory.
2. Open `life_expectancy.ipynb` in Jupyter Notebook or VS Code.
3. Run the notebook cells in order.

---

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

Install dependencies with:
```
pip install pandas numpy matplotlib seaborn scikit-learn
```

---

## Key Steps

1. **Exploratory Data Analysis (EDA):**
   - Inspect data structure, missing values, and summary statistics.
   - Visualize the distribution of life expectancy.
   - Explore feature correlations.

2. **Data Preprocessing:**
   - Drop categorical columns for simplicity.
   - Impute missing values with the mean.
   - Split data into training and test sets.
   - Normalize features.

3. **Modeling:**
   - Implement linear regression from scratch (gradient descent) This is the hard part of the project.
   - Train and evaluate both custom and scikit-learn models.
   - Compare model coefficients and prediction performance.

4. **Visualization:**
   - Plot training loss curve for the custom model (This is very hard to understand sometimes).
   - Visualize predictions vs. true values for both models.

---

## Business Value

Accurate life expectancy prediction helps:
- Identify key health and socio-economic drivers.
- Guide resource allocation and policy interventions.
- Monitor and improve population health outcomes.

---

## License


---

**Author:** 
Goodness Akyengo