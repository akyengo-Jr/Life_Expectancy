# Life Expectancy EDA Dashboard

An interactive Streamlit dashboard for exploring the Life Expectancy dataset, providing insights into factors affecting life expectancy across different countries and over time.

## Features

This dashboard replicates the analyses from the `exploratory_analysis.ipynb` notebook with added interactivity:

1. **Dataset Overview**
   - View the first 10 rows of data
   - Check dataset shape and column information
   - Identify missing values

2. **Target Variable Analysis**
   - Distribution of life expectancy with histogram and KDE
   - Descriptive statistics

3. **Feature Correlation Analysis**
   - Interactive correlation heatmap for all numeric features

4. **Key Features Analysis**
   - Distribution plots for GDP, Schooling, BMI, and Adult Mortality
   - Select which features to visualize

5. **Country Status Analysis**
   - Distribution of countries by development status (Developed vs Developing)

6. **Bivariate Relationships**
   - Scatter plots showing relationships between life expectancy and key features
   - Life expectancy vs GDP by country status

7. **Temporal Trends**
   - Line plot showing life expectancy trends over time by country status

8. **Distribution and Outliers Analysis**
   - Boxplots for selected numerical variables

9. **EDA Insights**
   - Key findings for the modeling phase

## Interactive Components

- **Country Status Filter**: Select between All, Developing, or Developed countries
- **Year Range Slider**: Filter data by specific year ranges (if Year column exists)
- **Feature Selection**: Choose which features to analyze in distribution and scatter plots
- **Column Selection**: Select which numerical columns to include in boxplot analysis

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy

## Installation

1. Clone the repository or download the files
2. Install the required packages:
   ```bash
   pip install streamlit pandas matplotlib seaborn numpy
   ```

## Usage

1. Ensure the `cleaned_data.csv` file is in the `Life_Expectancy` directory
2. Run the Streamlit app:
   ```bash
   cd Life_Expectancy
   streamlit run eda_app.py
   ```
3. The app will open in your default web browser at `http://localhost:8501`

## Data

The dashboard uses the `cleaned_data.csv` file which should be the output of the data wrangling process. This dataset contains various health, demographic, and economic indicators for multiple countries over several years.

## Dashboard Sections

### Dataset Overview
Provides basic information about the dataset including shape, columns, and missing values.

### Target Variable Analysis
Visualizes the distribution of the life expectancy variable with descriptive statistics.

### Feature Correlation Analysis
Shows the correlation between all numeric features in the dataset using a heatmap.

### Key Features Analysis
Displays distribution plots for key features (GDP, Schooling, BMI, Adult Mortality) with the ability to select which features to display.

### Country Status Analysis
Shows the distribution of countries by development status (Developed vs Developing).

### Bivariate Relationships
Visualizes relationships between life expectancy and key features using scatter plots.

### Life Expectancy vs GDP by Country Status
Shows how life expectancy relates to GDP, differentiated by country development status.

### Temporal Trends
Displays life expectancy trends over time, separated by country development status.

### Distribution and Outliers Analysis
Boxplots for selected numerical variables to identify outliers and distributions.

### EDA Insights
Key findings from the exploratory data analysis that inform the modeling phase.

## Customization

You can modify the app by editing `eda_app.py`:
- Add new visualizations
- Modify existing plots
- Add new filters
- Change the layout

## Troubleshooting

If you encounter issues:
1. Ensure all required packages are installed
2. Verify that `cleaned_data.csv` is in the correct directory
3. Check that the data file has the expected columns
4. Restart the Streamlit server if changes aren't reflected

## Contributing

Feel free to fork this project and submit pull requests with improvements or additional features.
