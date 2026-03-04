# Life Expectancy Analysis & Interactive Dashboard

This is my project where I explore the "Life Expectancy Data.csv" dataset to understand what factors influence how long people live in different countries. I focused on exploratory data analysis and built an interactive web app using Streamlit so anyone can explore the data and make predictions without writing code.

---

## What I Wanted to Find Out

- **Main Goal:** Understand which health, economic, and social factors actually matter for life expectancy
- **How I Did It:** 
  - Dug into the data with lots of visualizations to spot patterns
  - Built a simple web app where you can play with the data yourself
  - Made it possible to predict life expectancy by adjusting different factors

---

## What's in This Project

- **data_wrangling.ipynb and exploratory_analysis.ipynb**: notebooks where I did all the data cleaning preparing it for the EDA process
- **eda_app.py**: The Streamlit app code (run this to launch the dashboard)
- **Life Expectancy Data.csv**: The dataset from WHO (you'll need to add this yourself in the data wrangling notebook to clean it)
- **requirements.txt**: List of packages you need to install

---

## How to Run My Project

### For the Analysis Notebook:
1. Put `Life Expectancy Data.csv` in the project folder
2. Open `data_wrangling.ipynb` in Jupyter
3. Run each cell to clean the data.
4. Open the `exploratory_analysis.ipynb` in Jupyter and run the cells to see what i found out

### For the Interactive Dashboard:
1. Install everything first (see below)
2. In your terminal, type:
   ```bash
   streamlit run eda_app.py
   ```
3. Your browser should open automatically - if not, go to http://localhost:8501

---

## What You Need Installed

- Python 3.8 or newer
- pandas (for working with data)
- numpy (for calculations)
- matplotlib & seaborn (for basic graphs)
- plotly (for interactive charts in the dashboard)
- scikit-learn (for the prediction model)
- streamlit (for the web app)

Just run this to get everything:
```bash
pip install -r requirements.txt
```

Or if you prefer to install one by one:
```bash
pip install pandas numpy matplotlib seaborn plotly scikit-learn streamlit
```

---

## What I Found in the Data

I spent a lot of time just looking at the data and making graphs. Here's what stood out:

### 1. First Look:
- Checked for missing data (there's quite a bit)
- Looked at basic stats for each column
- Saw that life expectancy varies a lot between countries

### 2. Over Time:
- Most countries are living longer than they used to
- But the gap between rich and poor countries is still huge
- Some countries actually went backwards in some years

### 3. What Matters Most:
- **Adult mortality** has the strongest negative relationship (makes sense)
- **Immunization rates** (especially Hepatitis B and DPT) really matter
- **GDP per capita** - richer countries = longer lives, but it's not a straight line
- **Schooling** - more years in school = longer life expectancy
- **Alcohol consumption** - moderate amounts don't seem bad, but heavy drinking areas have issues

### 4. Developed vs Developing:
- Huge gap - developed countries average ~80 years, developing ~65-70
- The gap is slowly closing but not fast enough

### 5. Interesting Patterns:
- Thinness and life expectancy have a weird relationship (probably because thinness in poor countries means hunger, in rich countries it's sometimes a choice)
- HIV/AIDS completely changes the picture for some African countries
- Healthcare spending helps but only up to a point - after a certain level, more money doesn't add many years

---

## What the Dashboard Does

I wanted to make something non-technical people could use:

- **Explore the Data:** Pick countries, years, and variables to see custom graphs
- **Make Predictions:** Slide bars to change things like healthcare spending or immunization rates and see how life expectancy changes instantly
- **Compare Countries:** See two countries side by side
- **Download Stuff:** Save graphs or prediction (I plan to add this later on) results if you want

---

## Why This Matters

I think this could actually be useful for:
- **Health officials:** See which interventions might make the biggest difference
- **Students:** Understand how data science applies to real-world problems
- **Journalists:** Find stories in the data about health inequalities
- **Anyone curious:** Play with the data themselves instead of just reading about it

---

## Try It Yourself

The dashboard is easy to run locally. If enough people find it useful, I might put it online permanently so anyone can access it without installing anything.

---

**Made by:** Goodness Akyengo
