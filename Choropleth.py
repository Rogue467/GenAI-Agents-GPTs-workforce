import streamlit as st
import folium
import json
from streamlit_folium import folium_static
import pandas as pd

def create_choropleth_app():
    st.title("Bangalore Pincode Level Choropleth Map")
    
    try:
        # Load GeoJSON data
        with open('boundary.geojson', 'r') as f:
            bangalore_geojson = json.load(f)
        
        # Create sample pincode data
        pincode_data = {
            'Pincode': ['560001', '560002', '560003', '560004', '560005'],
            'Area': ['MG Road', 'Shivajinagar', 'Ulsoor', 'RT Nagar', 'Benson Town'],
            'Metric': [75, 82, 65, 90, 70]
        }
        df = pd.DataFrame(pincode_data)
        
        # Create base map
        m = folium.Map(
            location=[12.9716, 77.5946],
            zoom_start=11,
            tiles='CartoDB positron'
        )
        
        # Add choropleth layer
        folium.Choropleth(
            geo_data=bangalore_geojson,
            data=df,
            columns=['Pincode', 'Metric'],
            key_on='feature.properties.pin_code',  # Changed from 'pincode' to 'pin_code'
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Metric Value'
        ).add_to(m)
        
        # Display map
        folium_static(m)
        
        # Add controls
        st.sidebar.header("Filters")
        metric_range = st.sidebar.slider(
            "Filter by Metric",
            min_value=int(df['Metric'].min()),
            max_value=int(df['Metric'].max()),
            value=(int(df['Metric'].min()), int(df['Metric'].max()))
        )
        
    except FileNotFoundError:
        st.error("Please ensure the GeoJSON file is in the correct location")
        
if __name__ == "__main__":
    create_choropleth_app()

# Add this after loading GeoJSON
st.write(bangalore_geojson['features'][0]['properties'].keys())
