

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 DataLens", layout="wide")

theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])

if theme == "Dark":
    dark_theme_css = """
        <style>
        body, .stApp { background-color: #121212 !important; color: white !important; }
        .css-1d391kg, .css-1n76uvr { background-color: #121212 !important; }
        .css-qri22k, .css-10trblm, .css-1v0mbdj, .stTextInput, .stSelectbox, .stMultiSelect, .stRadio { 
            color: white !important; 
        }
        .stButton>button { 
            background-color: #1f77b4 !important; 
            color: white !important; 
            border: 1px solid white !important;
        }
        .stButton>button:hover { 
            background-color: #0d6efd !important; 
        }
        </style>
    """
    st.markdown(dark_theme_css, unsafe_allow_html=True)

st.title("📊 DataLens")

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

uploaded_file = st.file_uploader("📂 Upload a CSV file", type="csv")

if uploaded_file:
    df = load_data(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.write(df.head())

    st.subheader("📊 Data Summary")
    st.write(df.describe())

    st.sidebar.subheader("🔎 Filter Data")
    columns = df.columns.tolist()

    selected_column = st.sidebar.selectbox("Select column to filter by:", columns)
    unique_values = df[selected_column].unique()
    selected_values = st.sidebar.multiselect("Select Values:", unique_values)

    filter_df = df[df[selected_column].isin(selected_values)] if selected_values else df
    st.write(filter_df)

    st.sidebar.subheader("📈 Plot Settings")
    x_column = st.sidebar.selectbox("Select X-axis column:", columns)
    y_column = st.sidebar.selectbox("Select Y-axis column:", columns)
    plot_type = st.sidebar.radio("Choose Plot Type:", ["Bar Chart", "Line Chart", "Scatter Plot"])

    if st.sidebar.button("Generate Plot"):
        if not filter_df.empty:
            fig, ax = plt.subplots(figsize=(8, 5))

            if plot_type == "Bar Chart":
                ax.bar(filter_df[x_column], filter_df[y_column], color="skyblue")
            elif plot_type == "Line Chart":
                ax.plot(filter_df[x_column], filter_df[y_column], marker="o", linestyle="-", color="green")
            elif plot_type == "Scatter Plot":
                ax.scatter(filter_df[x_column], filter_df[y_column], color="red")

            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f"{plot_type} of {y_column} vs {x_column}")
            st.pyplot(fig)
        else:
            st.warning("No data available for the selected filter.")

    st.subheader("📌 Additional Data Insights")
    
    st.subheader("📌 Correlation Matrix")
    numerical_df = df.select_dtypes(include=["number"])  # Select only numerical columns
    if not numerical_df.empty:
       st.write(numerical_df.corr())
    else:
       st.warning("No numerical columns available for correlation.")


    st.subheader("📌 Missing Values")
    missing_values = df.isnull().sum()
    st.write(missing_values[missing_values > 0])

    st.subheader("📌 Aggregation")
    agg_column = st.selectbox("Select column for aggregation:", columns)
    agg_func = st.selectbox("Select aggregation function:", ["Sum", "Mean", "Median", "Max", "Min"])
    if st.button("Compute Aggregation"):
        if agg_func == "Sum":
            result = df[agg_column].sum()
        elif agg_func == "Mean":
            result = df[agg_column].mean()
        elif agg_func == "Median":
            result = df[agg_column].median()
        elif agg_func == "Max":
            result = df[agg_column].max()
        elif agg_func == "Min":
            result = df[agg_column].min()
        st.write(f"{agg_func} of {agg_column}: {result}")

    st.subheader("📌 Sort Data")
    sort_column = st.selectbox("Select column to sort by:", columns)
    ascending = st.radio("Sort Order:", ["Ascending", "Descending"])
    if st.button("Sort Data"):
        sorted_df = df.sort_values(by=sort_column, ascending=(ascending == "Ascending"))
        st.write(sorted_df)

    st.subheader("📌 Unique Value Counts")
    unique_column = st.selectbox("Select column to count unique values:", columns)
    if st.button("Show Unique Values"):
        st.write(df[unique_column].value_counts())
else:
    st.info("Please upload a CSV file to continue.")
