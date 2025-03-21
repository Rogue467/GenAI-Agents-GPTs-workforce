import streamlit as st
import pandas as pd
import plotly.express as px

def create_events_dashboard():
    st.title("Insider's Top NYE 2025 Events Dashboard")

    # Create events dataframe
    events_data = {
        'Event Name': [
            'Skyfall 2025 NYE',
            'Hyderabad Biggest New Year Bash',
            'Elitify 2025',
            'Party Paradise 2025',
            'One Night In Vegas 2025'
        ],
        'City': [
            'Bangalore',
            'Hyderabad',
            'Kolkata',
            'Chennai',
            'Bangalore'
        ],
        'Venue': [
            'Gatsby Cocktails & Cuisines',
            'Hitech Arena',
            'PC Chandra Garden',
            'Ramada by Wyndham',
            'Hoot Cafe & Brewery'
        ],
        'Price': [999, 299, 4500, 2399, 2199],
        'Duration': [4, 6, 4, 5, 5.5],
        'Start_Time': ['8:00 PM', '7:01 PM', '9:15 PM', '7:00 PM', '7:30 PM']
    }
    
    df = pd.DataFrame(events_data)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_city = st.sidebar.multiselect(
        "Select Cities",
        options=df['City'].unique(),
        default=df['City'].unique()
    )
    
    price_range = st.sidebar.slider(
        "Price Range",
        min_value=int(df['Price'].min()),
        max_value=int(df['Price'].max()),
        value=(int(df['Price'].min()), int(df['Price'].max()))
    )
    
    # Filter data
    filtered_df = df[
        (df['City'].isin(selected_city)) &
        (df['Price'].between(price_range[0], price_range[1]))
    ]
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Comparison")
        fig_price = px.bar(
            filtered_df,
            x='Event Name',
            y='Price',
            color='City',
            title='Event Prices by City'
        )
        st.plotly_chart(fig_price)
    
    with col2:
        st.subheader("Events by City")
        fig_city = px.pie(
            filtered_df,
            names='City',
            title='Distribution of Events by City'
        )
        st.plotly_chart(fig_city)
    
    # Event details table
    st.subheader("Event Details")
    st.dataframe(
        filtered_df,
        column_config={
            "Event Name": st.column_config.TextColumn("Event Name", width="medium"),
            "Price": st.column_config.NumberColumn("Price (₹)", format="₹%d"),
            "Duration": st.column_config.NumberColumn("Duration (hours)")
        },
        hide_index=True
    )
    
    # Event highlights
    st.subheader("Event Highlights")
    for _, event in filtered_df.iterrows():
        with st.expander(f"🎉 {event['Event Name']}"):
            st.write(f"**Venue:** {event['Venue']}")
            st.write(f"**Start Time:** {event['Start_Time']}")
            st.write(f"**Duration:** {event['Duration']} hours")
            st.write(f"**Price:** ₹{event['Price']}")

if __name__ == "__main__":
    create_events_dashboard()
