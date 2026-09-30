import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. App Title and Description
st.title("📊 Interactive Data Dashboard")
st.markdown("Welcome to your Streamlit app. Modify this file to build your own dashboard.")

# 3. Sidebar for User Inputs / Navigation
st.sidebar.header("Settings")
user_name = st.sidebar.text_input("Enter your name:", "Guest")
sample_size = st.sidebar.slider("Select number of data points:", 10, 500, 100)

st.sidebar.write(f"Hello, {user_name}!")

# 4. Generate Mock Data (Replace with your own data source)
@st.cache_data  # Caches the data to make the app faster
def load_data(rows):
    df = pd.DataFrame(
        np.random.randn(rows, 3),
        columns=['Metric A', 'Metric B', 'Metric C']
    )
    return df

data = load_data(sample_size)

# 5. Main Layout - Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Data Summary")
    st.dataframe(data.head())  # Displays an interactive table

with col2:
    st.subheader("Data Visualization")
    st.line_chart(data)  # Displays a native Streamlit line chart

# 6. Status Elements / Interactivity
if st.button("Celebrate!"):
    st.balloons()
    st.success("Cheers to your new app!")
