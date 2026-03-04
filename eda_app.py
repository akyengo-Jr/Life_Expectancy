import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Page config - keeping this simple
st.set_page_config(
    page_title="Life Expectancy Analysis",
    page_icon="📊",
    layout="wide"
)

# Title - keeping it clean
st.title("Life Expectancy Exploratory Data Analysis")
st.markdown("""
Just me digging into the Life Expectancy dataset to understand what actually affects how long people live. 
Play around with the filters on the left - that's where all the action starts.
""")

# Load data - this took me a while to figure out the caching thing
@st.cache_data
def load_data():
    # had some issues with file paths initially
    data = pd.read_csv('data/cleaned_data.csv')
    return data

try:
    data = load_data()
    st.success("Data loaded successfully !")
except FileNotFoundError:
    st.error("Can't find the cleaned_data.csv file. Make sure it's in the right folder.")
    st.stop()

# Sidebar filters - spent a lot of time thinking about what filters actually make sense
st.sidebar.header("Filters")

# Status filter - developing vs developed always interesting to compare
status_options = ['All'] + list(data['Status'].unique())
selected_status = st.sidebar.selectbox("Country Status", status_options)

# Year filter - wanted to see how things change over time
if 'Year' in data.columns:
    min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
    selected_years = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))
else:
    selected_years = None

# Country selector - realized sometimes you just want to focus on specific places
countries = sorted(data['Country'].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Pick Specific Countries (if you want)",
    options=countries,
    default=[]
)

# Apply filters - this part was tricky but I think I got it right
filtered_data = data.copy()
if selected_status != 'All':
    filtered_data = filtered_data[filtered_data['Status'] == selected_status]
    
if selected_years and 'Year' in filtered_data.columns:
    filtered_data = filtered_data[
        (filtered_data['Year'] >= selected_years[0]) & 
        (filtered_data['Year'] <= selected_years[1])
    ]

if selected_countries:
    filtered_data = filtered_data[filtered_data['Country'].isin(selected_countries)]

# Quick stats - helps me get a feel for what I'm working with
st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
st.sidebar.metric("Records", f"{len(filtered_data):,}")
st.sidebar.metric("Countries", filtered_data['Country'].nunique())
st.sidebar.metric("Avg Life Expectancy", f"{filtered_data['Life expectancy'].mean():.1f} years")

# Using tabs to keep things organized - got this idea from another project
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Data Overview", 
    "Distributions", 
    "Relationships", 
    "Trends Over Time",
    "Country Deep Dive"
])

with tab1:
    st.header("First Look at the Data")
    
    # Always good to see what you're dealing with
    st.subheader("First Few Rows")
    st.dataframe(filtered_data.head(10), use_container_width=True)
    
    # I like checking missing values early - saves headaches later
    st.subheader("Missing Values Check")
    missing_df = filtered_data.isnull().sum().reset_index()
    missing_df.columns = ['Column', 'Missing']
    missing_df = missing_df[missing_df['Missing'] > 0]
    
    if not missing_df.empty:
        fig = px.bar(
            missing_df, 
            x='Column', 
            y='Missing',
            title="Where are the gaps?",
            color='Missing',
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # my thoughts on missing data
        st.info("Hmm, quite a few missing values in some columns. Going to need to think about how to handle these for any modeling. Population and GDP have the most gaps - not surprising since poorer countries might not report consistently.")
    else:
        st.success("No missing values - that's because I'm I already cleaned it using the data wrangling notebook!")
    
    # Dataset shape and basic info
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dataset Shape")
        st.write(f"Rows: {len(filtered_data):,}")
        st.write(f"Columns: {len(filtered_data.columns)}")
    
    with col2:
        st.subheader("Data Types")
        dtypes_df = pd.DataFrame({
            'Column': filtered_data.dtypes.index,
            'Type': filtered_data.dtypes.values.astype(str)
        })
        st.dataframe(dtypes_df, use_container_width=True)

with tab2:
    st.header("How Things Are Distributed")
    
    # This is where I spent most of my time - distributions tell you so much
    numeric_cols = filtered_data.select_dtypes(include=[np.number]).columns.tolist()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_var = st.selectbox(
            "Pick a variable to explore",
            options=numeric_cols,
            index=numeric_cols.index('Life expectancy') if 'Life expectancy' in numeric_cols else 0
        )
        
        chart_type = st.radio(
            "Chart type",
            ["Histogram", "Box Plot", "Violin Plot"]
        )
        
        split_by_status = st.checkbox("Split by developed/developing", value=True)
    
    with col2:
        if chart_type == "Histogram":
            fig = px.histogram(
                filtered_data, 
                x=selected_var,
                color='Status' if split_by_status and 'Status' in filtered_data.columns else None,
                marginal="box",
                title=f"Distribution of {selected_var}",
                nbins=40,
                opacity=0.7
            )
        elif chart_type == "Box Plot":
            fig = px.box(
                filtered_data,
                y=selected_var,
                x='Status' if split_by_status and 'Status' in filtered_data.columns else None,
                color='Status' if split_by_status and 'Status' in filtered_data.columns else None,
                title=f"Box plot of {selected_var}",
                points="outliers"
            )
        else:  # Violin Plot
            fig = px.violin(
                filtered_data,
                y=selected_var,
                x='Status' if split_by_status and 'Status' in filtered_data.columns else None,
                color='Status' if split_by_status and 'Status' in filtered_data.columns else None,
                box=True,
                points="all",
                title=f"Violin plot of {selected_var}"
            )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # My observations based on what I'm seeing
    if selected_var == 'Life expectancy':
        st.markdown("""
        **What I'm noticing:** Life expectancy isn't perfectly normal - there's a bit of a left skew. 
        That means quite a few countries are pulling the average down. The developing vs developed split 
        is huge though - developed countries are all clustered up near 80, while developing countries 
        are all over the place from the 40s to the 80s.
        """)
    elif selected_var == 'GDP':
        st.markdown("""
        **My take:** GDP is massively skewed. Most countries have relatively low GDP, with a few rich 
        countries way out on the right. This is going to need a log transform if I do any modeling - 
        can't have one variable dominating everything.
        """)
    elif selected_var == 'Adult Mortality':
        st.markdown("""
        **Interesting:** Adult mortality has a long tail - some countries have rates that are 
        shockingly high. The box plot shows quite a few outliers. Probably related to HIV/AIDS 
        in some African countries (Just a thought though).
        """)

with tab3:
    st.header("How Variables Relate to Each Other")
    
    # This is where it gets interesting - seeing what actually matters
    col1, col2 = st.columns([1, 3])
    
    with col1:
        x_var = st.selectbox("X axis", options=numeric_cols, index=0)
        y_var = st.selectbox("Y axis", options=numeric_cols, index=numeric_cols.index('Life expectancy') if 'Life expectancy' in numeric_cols else 1)
        
        color_var = st.selectbox(
            "Color by (optional)",
            options=['None'] + [col for col in filtered_data.columns if col not in [x_var, y_var]],
            index=0
        )
        
        add_trend = st.checkbox("Add trend line", value=True)
    
    with col2:
        fig = px.scatter(
            filtered_data,
            x=x_var,
            y=y_var,
            color=None if color_var == 'None' else color_var,
            hover_data=['Country', 'Year'] if 'Country' in filtered_data.columns else None,
            trendline="ols" if add_trend else None,
            title=f"{y_var} vs {x_var}",
            opacity=0.6
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Sharing what I'm seeing in these relationships
    if x_var == 'GDP' and y_var == 'Life expectancy':
        st.markdown("""
        **What jumps out at me:** There's definitely a relationship, but it's not linear. 
        Once countries hit a certain GDP level (maybe around 20000-30000), life expectancy 
        doesn't improve much more. The developing countries show huge variation at low GDP levels 
        - meaning money isn't the whole story. Something else is going on there.
        """)
    elif x_var == 'Schooling' and y_var == 'Life expectancy':
        st.markdown("""
        **This one's clear:** More schooling = longer life, pretty consistently. 
        The relationship looks almost linear. Makes sense - education probably means better 
        health literacy, better jobs, better access to healthcare. No country with high 
        schooling has low life expectancy.
        """)
    
    # Correlation heatmap - always useful to see the big picture
    st.subheader("Correlation Matrix")
    
    # Let user pick which variables to include
    corr_cols = st.multiselect(
        "Pick variables for correlation",
        options=numeric_cols,
        default=['Life expectancy', 'Adult Mortality', 'GDP', 'Schooling', 'BMI'][:min(5, len(numeric_cols))]
    )
    
    if len(corr_cols) >= 2:
        corr_matrix = filtered_data[corr_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title="How everything connects"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # My summary of what the correlations tell me
        st.markdown("""
        **Main takeaways from correlations:**
        - Adult mortality is the strongest negative predictor (no surprise there)
        - Schooling and GDP both correlate positively and strongly
        - BMI has a weird relationship - probably because in poor countries low BMI means malnutrition, 
          in rich countries high BMI means obesity. Need to be careful with this one.
        - Immunization variables all cluster together - if a country does one well, they probably do them all well.
        """)

with tab4:
    st.header("How Things Change Over Time")
    
    if 'Year' in filtered_data.columns:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            trend_var = st.selectbox(
                "What to track over time",
                options=numeric_cols,
                index=numeric_cols.index('Life expectancy') if 'Life expectancy' in numeric_cols else 0
            )
            
            # Different ways to aggregate - each tells a different story
            agg_method = st.selectbox(
                "Aggregation method",
                ["Mean", "Median", "Min", "Max"]
            )
            
            group_status = st.checkbox("Split by status", value=True)
            show_countries = st.checkbox("Show selected countries", value=False)
        
        with col2:
            # Had to look up how to do this grouping properly
            if group_status and 'Status' in filtered_data.columns:
                if agg_method == "Mean":
                    trend_data = filtered_data.groupby(['Year', 'Status'])[trend_var].mean().reset_index()
                elif agg_method == "Median":
                    trend_data = filtered_data.groupby(['Year', 'Status'])[trend_var].median().reset_index()
                elif agg_method == "Min":
                    trend_data = filtered_data.groupby(['Year', 'Status'])[trend_var].min().reset_index()
                else:
                    trend_data = filtered_data.groupby(['Year', 'Status'])[trend_var].max().reset_index()
                
                fig = px.line(
                    trend_data,
                    x='Year',
                    y=trend_var,
                    color='Status',
                    title=f"{agg_method} {trend_var} over time",
                    markers=True
                )
            else:
                if agg_method == "Mean":
                    trend_data = filtered_data.groupby('Year')[trend_var].mean().reset_index()
                elif agg_method == "Median":
                    trend_data = filtered_data.groupby('Year')[trend_var].median().reset_index()
                elif agg_method == "Min":
                    trend_data = filtered_data.groupby('Year')[trend_var].min().reset_index()
                else:
                    trend_data = filtered_data.groupby('Year')[trend_var].max().reset_index()
                
                fig = px.line(
                    trend_data,
                    x='Year',
                    y=trend_var,
                    title=f"{agg_method} {trend_var} over time",
                    markers=True
                )
            
            # Overlay individual countries if user wants - can get messy though
            if show_countries and selected_countries:
                country_data = filtered_data[filtered_data['Country'].isin(selected_countries)]
                # This adds the individual lines - hope it's not too cluttered
                for trace in px.line(country_data, x='Year', y=trend_var, color='Country').data:
                    fig.add_trace(trace)
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # My observations on trends
        if trend_var == 'Life expectancy':
            st.markdown("""
            **What the trend tells me:** Globally, life expectancy is going up - that's the good news. 
            But look at the gap between developed and developing countries. It's shrinking, but slowly. 
            The minimum line is interesting - the worst-off countries are improving, but there are still 
            places where people die young.
            """)
        
        # Year-over-year changes - shows volatility
        st.subheader("Year-over-Year Changes")
        
        if len(trend_data) > 1:
            trend_data['Change'] = trend_data[trend_var].pct_change() * 100
            
            fig = px.bar(
                trend_data,
                x='Year',
                y='Change',
                color='Change' if 'Status' not in trend_data.columns else 'Status',
                title=f"Percent change in {trend_var} from previous year",
                barmode='group' if 'Status' in trend_data.columns else 'relative'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Notice:** The year-to-year changes are usually small (1-2%), but sometimes there are big jumps. 
            Those big jumps usually happen in countries that had some kind of crisis or major improvement. 
            Would be interesting to dig into those cases separately.
            """)
    else:
        st.warning("No Year column - can't do time analysis")

with tab5:
    st.header("Country-Level Deep Dive")
    
    # This is where I can really see the stories in the data
    col1, col2 = st.columns([1, 2])
    
    with col1:
        rank_var = st.selectbox(
            "Rank countries by",
            options=numeric_cols,
            index=numeric_cols.index('Life expectancy') if 'Life expectancy' in numeric_cols else 0
        )
        
        rank_direction = st.radio(
            "Show me",
            ["Top 10", "Bottom 10"]
        )
        
        if 'Year' in data.columns:
            rank_year = st.slider(
                "Year",
                min_value=int(data['Year'].min()),
                max_value=int(data['Year'].max()),
                value=int(data['Year'].max()),
                step=1
            )
        else:
            rank_year = None
    
    with col2:
        if rank_year:
            year_data = filtered_data[filtered_data['Year'] == rank_year].dropna(subset=[rank_var])
            
            if rank_direction == "Top 10":
                ranked = year_data.nlargest(10, rank_var)[['Country', rank_var, 'Status']]
                title = f"Top 10 by {rank_var} ({rank_year})"
            else:
                ranked = year_data.nsmallest(10, rank_var)[['Country', rank_var, 'Status']]
                title = f"Bottom 10 by {rank_var} ({rank_year})"
            
            fig = px.bar(
                ranked,
                x=rank_var,
                y='Country',
                color='Status',
                orientation='h',
                title=title,
                text=rank_var,
                color_discrete_map={'Developed': 'blue', 'Developing': 'orange'}
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # My thoughts on the rankings
            if rank_var == 'Life expectancy' and rank_direction == "Top 10":
                st.markdown("""
                **Look at this:** The top countries are almost all developed - Japan, Switzerland, Australia etc. 
                But notice some developing countries sneak in? That's interesting - means you don't have to be rich 
                to have a healthy population. Cuba's a famous example - good health outcomes without being wealthy.
                """)
            elif rank_var == 'Life expectancy' and rank_direction == "Bottom 10":
                st.markdown("""
                **This is sobering:** All developing countries, mostly in sub-Saharan Africa. 
                Sierra Leone, Central African Republic, Chad keep showing up. The gap between 
                top and bottom is huge - like 30+ years difference. That's not right.
                """)
    
    # Compare specific countries - this was a pain to code but worth it
    st.subheader("Compare Countries Side by Side")
    
    compare_list = st.multiselect(
        "Pick countries to compare",
        options=sorted(data['Country'].unique()),
        default=sorted(data['Country'].unique())[:3] if len(data['Country'].unique()) >= 3 else []
    )
    
    if compare_list and 'Year' in data.columns:
        compare_vars = st.multiselect(
            "What to compare",
            options=numeric_cols,
            default=['Life expectancy', 'GDP', 'Schooling'][:min(3, len(numeric_cols))]
        )
        
        if compare_vars:
            compare_data = filtered_data[filtered_data['Country'].isin(compare_list)]
            
            # Create subplots - one for each variable
            fig = make_subplots(
                rows=len(compare_vars),
                cols=1,
                subplot_titles=compare_vars,
                shared_xaxes=True,
                vertical_spacing=0.1
            )
            
            for i, var in enumerate(compare_vars, 1):
                for country in compare_list:
                    country_data = compare_data[compare_data['Country'] == country]
                    fig.add_trace(
                        go.Scatter(
                            x=country_data['Year'],
                            y=country_data[var],
                            name=f"{country}",
                            legendgroup=country,
                            showlegend=(i == 1)
                        ),
                        row=i, col=1
                    )
            
            fig.update_layout(height=300 * len(compare_vars), title_text="Country Comparison")
            st.plotly_chart(fig, use_container_width=True)
            
            # My take on comparisons
            st.markdown("""
            **What I like about this view:** You can really see how countries diverge. 
            Some start at similar places but take different paths. Others are completely 
            different from the beginning. Always makes me wonder about the historical 
            and political factors that aren't in this dataset.
            """)

# Final thoughts section - tried to summarize what I learned
st.markdown("---")
st.header("What I Learned from All This")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Things That Matter Most")
    st.write("""
    - Adult mortality is the biggest red flag
    - Education matters as much as money, maybe more
    - Immunization programs work - the data backs this up
    - Being a developed country helps, but it's not everything
    """)

with col2:
    st.subheader("Data Quirks to Remember")
    st.write("""
    - GDP needs a log transform if I model this
    - Missing data is a real issue in some columns
    - BMI is tricky - means different things in different contexts
    - Outliers aren't always errors - they're real countries with real problems
    """)

with col3:
    st.subheader("Questions I Still Have")
    st.write("""
    - Why do some poor countries do so well?
    - What caused the big drops in some countries?
    - Is the developing/developed split still useful?
    - What's not in this data that matters?
    """)

# Footer with download option - someone might want the filtered data
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("Life Expectancy Analysis - my little exploration project")
    
    # Let people download what I'm looking at
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download this filtered data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )
