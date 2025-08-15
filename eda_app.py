import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Set page config
st.set_page_config(
    page_title="Life Expectancy EDA",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Life Expectancy Exploratory Data Analysis")
st.markdown("""
This interactive dashboard explores the Life Expectancy dataset, providing insights into factors affecting life expectancy across different countries and over time.
""")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('cleaned_data.csv')
    return data

try:
    data = load_data()
    st.success("Data loaded successfully!")
except FileNotFoundError:
    st.error("Data file not found. Please ensure 'Life_Expectancy/cleaned_data.csv' exists.")
    st.stop()

# Sidebar for filters
st.sidebar.header("Filters")

# Country status filter
status_options = ['All'] + list(data['Status'].unique())
selected_status = st.sidebar.selectbox("Select Country Status", status_options)

# Year range filter
if 'Year' in data.columns:
    min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
    selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
else:
    selected_years = None

# Filter data based on selections
filtered_data = data.copy()
if selected_status != 'All':
    filtered_data = filtered_data[filtered_data['Status'] == selected_status]
    
if selected_years and 'Year' in filtered_data.columns:
    filtered_data = filtered_data[
        (filtered_data['Year'] >= selected_years[0]) & 
        (filtered_data['Year'] <= selected_years[1])
    ]

# Data overview
st.header("Dataset Overview")
st.subheader("First 10 Rows of Data")
st.dataframe(filtered_data.head(10))

col1, col2 = st.columns(2)
with col1:
    st.subheader("Dataset Info")
    st.write(f"Shape: {filtered_data.shape}")
    st.write(f"Columns: {len(filtered_data.columns)}")
    
with col2:
    st.subheader("Missing Values")
    missing_values = filtered_data.isnull().sum()
    st.write(missing_values[missing_values > 0] if missing_values.sum() > 0 else "No missing values")

# Target variable distribution
st.header("Target Variable Analysis")
st.subheader("Distribution of Life Expectancy")

# Create figure with matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data['Life expectancy'], kde=True, ax=ax)
ax.set_title('Distribution of Life Expectancy')
st.pyplot(fig)

# Display statistics
st.subheader("Life Expectancy Statistics")
st.write(filtered_data['Life expectancy'].describe())

# Feature correlation
st.header("Feature Correlation Analysis")
st.subheader("Correlation Heatmap")

# Select only numeric columns for correlation
numeric_data = filtered_data.select_dtypes(include=[np.number])

# Create correlation matrix
corr_matrix = numeric_data.corr()

# Plot heatmap
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
ax.set_title('Feature Correlation Heatmap')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
st.pyplot(fig)

# Key features analysis
st.header("Key Features Analysis")

# Select features for analysis
features = ['GDP', 'Schooling', 'BMI', 'Adult Mortality']
selected_features = st.multiselect(
    "Select features to analyze", 
    features, 
    default=features
)

if selected_features:
    # Distribution plots
    st.subheader("Feature Distributions")
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()
    
    for i, col in enumerate(selected_features):
        if i < 4:  # Only plot up to 4 features
            sns.histplot(filtered_data[col], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {col}')
    
    # Hide unused subplots
    for j in range(len(selected_features), 4):
        axes[j].set_visible(False)
        
    plt.tight_layout()
    st.pyplot(fig)

# Country status analysis
st.header("Country Status Analysis")
if 'Status' in filtered_data.columns:
    status_counts = filtered_data['Status'].value_counts(normalize=True)
    st.subheader("Country Status Distribution")
    st.write(status_counts)
    
    # Plot status distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x='Status', data=filtered_data, ax=ax)
    ax.set_title('Distribution of Country Status')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Developing', 'Developed'])
    st.pyplot(fig)

# Bivariate relationships
st.header("Bivariate Relationships")
st.subheader("Life Expectancy vs Key Features")

if selected_features:
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, col in enumerate(selected_features):
        if i < 4:  # Only plot up to 4 features
            sns.scatterplot(x=filtered_data[col], y=filtered_data['Life expectancy'], ax=axes[i])
            axes[i].set_title(f'Life Expectancy vs {col}')
    
    # Hide unused subplots
    for j in range(len(selected_features), 4):
        axes[j].set_visible(False)
        
    plt.tight_layout()
    st.pyplot(fig)

# Life expectancy vs GDP by status
st.header("Life Expectancy vs GDP by Country Status")
if 'GDP' in filtered_data.columns and 'Status' in filtered_data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='GDP', y='Life expectancy', hue='Status', data=filtered_data, alpha=0.6, ax=ax)
    ax.set_title('Life Expectancy vs GDP by Country Status')
    st.pyplot(fig)

# Temporal trends
st.header("Temporal Trends")
if 'Year' in filtered_data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='Year', y='Life expectancy', hue='Status', data=filtered_data, ax=ax)
    ax.set_title('Life Expectancy Trends Over Time')
    st.pyplot(fig)

# Boxplots for numerical variables
st.header("Distribution and Outliers Analysis")
st.subheader("Boxplots of Numerical Variables")

# Select columns for boxplot
numeric_columns = filtered_data.select_dtypes(include=[np.number]).columns.tolist()
selected_columns = st.multiselect(
    "Select columns for boxplot analysis", 
    numeric_columns, 
    default=['Life expectancy', 'GDP', 'Schooling', 'BMI', 'Adult Mortality']
)

if selected_columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=filtered_data[selected_columns], ax=ax)
    ax.tick_params(axis='x', rotation=45)
    ax.set_title('Boxplot of Selected Numerical Variables')
    st.pyplot(fig)

# EDA insights
st.header("EDA Insights for Modeling")
st.markdown("""
Based on the exploratory data analysis, here are key insights for the modeling phase:
""")

insights = {
    "Skewed Features": ["GDP", "Schooling"],
    "Important Predictors": ["Schooling", "Adult Mortality", "BMI", "GDP"],
    "Potential Interactions": [("GDP", "Status")]
}

for insight, items in insights.items():
    st.subheader(insight)
    if isinstance(items, list):
        for item in items:
            st.markdown(f"- {item}")
    elif isinstance(items, tuple):
        st.markdown(f"- {items[0]} and {items[1]}")

# Footer
st.markdown("---")
st.markdown("📊 Life Expectancy Exploratory Data Analysis Dashboard")
