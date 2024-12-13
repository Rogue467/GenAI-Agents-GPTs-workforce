import streamlit as st
import pandas as pd
import numpy as np

def calculate_rating_drops(df):
    # Group by program and break
    program_breaks = df[df['Level'] == 'Level 2'].copy()
    minute_ratings = df[df['Level'] == 'Level 4'].copy()
    
    results = []
    
    for program in program_breaks['Master Programme'].unique():
        prog_breaks = program_breaks[program_breaks['Master Programme'] == program]
        prog_minutes = minute_ratings[minute_ratings['Master Programme'] == program]
        
        for idx, ad_break in prog_breaks.iterrows():
            break_start = ad_break['Start Time']
            break_end = ad_break['End Time']
            break_rating = ad_break['F 22-40 ABC']
            
            # Get minute-by-minute ratings during break
            break_minutes = prog_minutes[
                (prog_minutes['Start Time'] >= break_start) & 
                (prog_minutes['End Time'] <= break_end)
            ]
            
            if not break_minutes.empty:
                # Calculate percentage drop for each minute
                minute_drops = ((break_minutes['F 22-40 ABC'] - break_rating) / break_rating) * 100
                
                results.append({
                    'Program': program,
                    'Break Start': break_start,
                    'Average Drop %': minute_drops.mean(),
                    'Break Duration': len(break_minutes)
                })
    
    return pd.DataFrame(results)

# Streamlit App
st.title("BARC Rating Drops Analysis")

# File upload
uploaded_file = st.file_uploader("Upload BARC Data CSV", type=['csv'])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # Add filters
    st.sidebar.header("Filters")
    selected_date = st.sidebar.selectbox(
        "Select Date",
        df['Date'].unique()
    )
    
    # Filter data by date
    filtered_df = df[df['Date'] == selected_date]
    
    # Calculate drops
    drops_df = calculate_rating_drops(filtered_df)
    
    # Display results
    st.header("Rating Drops by Program")
    
    # Summary metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Programs", len(drops_df['Program'].unique()))
    with col2:
        st.metric("Average Drop %", f"{drops_df['Average Drop %'].mean():.2f}%")
    
    # Detailed results
    st.dataframe(drops_df)
    
    # Visualization
    st.header("Rating Drops Visualization")
    
    import plotly.express as px
    fig = px.bar(
        drops_df,
        x='Program',
        y='Average Drop %',
        title='Average Rating Drops by Program',
        color='Break Duration'
    )
    st.plotly_chart(fig)
    
    # Download results
    csv = drops_df.to_csv(index=False)
    st.download_button(
        "Download Results",
        csv,
        "rating_drops.csv",
        "text/csv",
        key='download-csv'
    )
