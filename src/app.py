import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
from data_generator import create_sample_files
import plotly.express as px
from pipeline import process_sales_data
from PIL import Image
import time

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Sales Data Pipeline 🚀",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- HEADER SECTION -------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        color: #2F80ED;
        text-align: center;
        font-weight: bold;
        animation: fadeIn 1.5s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    .sub-title {
        text-align: center;
        color: #333333;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #2F80ED;
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B4D8C;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">💼 Sales Data Pipeline Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Generate synthetic sales data, clean it, transform it, and visualize the results</div>', unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.header("⚙️ Pipeline Controls")
target_date = st.sidebar.date_input("Select Date for Data Generation", datetime(2025, 9, 12))
st.sidebar.info("You can generate data for multiple dates or channels dynamically!")

# Paths
base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
input_dir = os.path.join(base_dir, 'input')
output_dir = os.path.join(base_dir, 'output')

# ------------------- MAIN APP -------------------

# Step 1: Generate Data
st.subheader("📥 Step 1: Generate Sales Data")
if st.button("Generate Records"):
    with st.spinner("Generating data files..."):
        create_sample_files(target_date=str(target_date))
        time.sleep(1)
    st.success(f"✅ Data generated successfully for {target_date}!")
    input_files = os.listdir(input_dir)
    

# Step 2: Process Data

if st.button("🔁 Transform & Process Data"):
    with st.spinner("Processing sales data..."):
        df = process_sales_data()  # internally calls pipeline
        st.success("✅ Data processed successfully!")

        # Load all output files
        output_path = os.path.join('data', 'output')
        daily_channel_summary = pd.read_csv(os.path.join(output_path, 'daily_channel_summary.csv'))
        top_5_products = pd.read_csv(os.path.join(output_path, 'top_5_products.csv'))
        daily_revenue = pd.read_csv(os.path.join(output_path, 'daily_revenue_summary.csv'))

        # Display all three datasets
        st.subheader("📊 Daily Channel Summary")
        st.dataframe(daily_channel_summary)

        st.subheader("💰 Daily Revenue Summary")
        st.dataframe(daily_revenue)

        st.subheader("🏆 Top 5 Best-Selling Products")
        st.dataframe(top_5_products)


# Step 3: View Outputs
st.markdown("## 🎨 Step 3: Visualize Final Data")
st.write("Here you can explore the final processed reports — total revenue, sales by channel, and top products.")

output_path = os.path.join('data', 'output')

if os.path.exists(os.path.join(output_path, 'daily_channel_summary.csv')):
    daily_channel_summary = pd.read_csv(os.path.join(output_path, 'daily_channel_summary.csv'))
    daily_revenue = pd.read_csv(os.path.join(output_path, 'daily_revenue_summary.csv'))
    top_5_products = pd.read_csv(os.path.join(output_path, 'top_5_products.csv'))

    # --- 1️⃣ Daily Channel Summary (Bar Chart) ---
    st.subheader("📊 Total Sales & Revenue by Channel (per day)")
    fig1 = px.bar(
        daily_channel_summary,
        x="date",
        y="total_revenue",
        color="channel",
        barmode="group",
        title="Total Revenue by Channel and Date",
        labels={"total_revenue": "Revenue", "date": "Date", "channel": "Sales Channel"},
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- 2️⃣ Daily Revenue Summary (Line Chart) ---
    

    # --- 3️⃣ Top 5 Products (Bar Chart) ---
    st.subheader("🏆 Top 5 Best-Selling Products by Date")
    fig3 = px.bar(
        top_5_products,
        x="product_id",
        y="total_revenue",
        color="product_id",
        facet_col="date",
        title="Top 5 Best-Selling Products (per day)",
        labels={"product_id": "Product ID", "total_revenue": "Revenue"},
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("⚠️ No processed data found. Please click **Transform & Process Data** first.")

# ------------------- FOOTER -------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#888;">
    🚀 Built with ❤️ using Streamlit | Sales Data Pipeline Demo
    </div>
    """,
    unsafe_allow_html=True
)
