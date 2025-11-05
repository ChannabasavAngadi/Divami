🛒 Sales Data Pipeline & Streamlit Dashboard
📘 Overview

This project simulates a Sales Data ETL pipeline that ingests synthetic sales data from multiple sales channels — Web App, Mobile App, and Physical Stores.
It cleans, aggregates, and reports insights such as:

✅ Total Sales per Channel

✅ Top 5 Best-Selling Products

✅ Total Revenue per Day

The processed data is saved in both CSV format and a SQLite database.
A Streamlit web app provides a user-friendly interface to generate data, transform it, and visualize insights beautifully with charts and animations.

📂 Project Structure
sales_data_pipeline/
├── data/
│   ├── input/                  # Auto-generated source CSVs
│   └── output/                 # Aggregated reports
├── src/
│   ├── data_generator.py       # Generates random sales data (for any given date)
│   ├── pipeline.py             # Cleans, aggregates, and stores data
│   └── app.py                  # Streamlit web app for visualization
├── sales_reports.db            # SQLite Database (created after running pipeline)
└── requirements.txt            # Required dependencies

⚙️ Setup Instructions
1️⃣ Clone the Repository
git clone https://github.com/yourusername/sales_data_pipeline.git
cd sales_data_pipeline

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Generate Sample Data

You can generate sample sales data for any specific date:

python src/data_generator.py


By default, the script creates CSVs under data/input/ for web_app, mobile_app, and physical_store.

4️⃣ Run the ETL Pipeline
python src/pipeline.py


This performs:

Data ingestion from CSVs

Cleaning invalid/missing values

Aggregation by channel and date

Identification of Top 5 best-selling products

Saves processed results to both data/output/ and SQLite DB

5️⃣ Run Streamlit Dashboard

Launch the interactive dashboard:

streamlit run src/app.py


Use the web UI to:

🎲 Generate new data

⚙️ Transform & Process it

📊 Visualize daily reports and top products

🔄 What the Pipeline Does
🧩 1. Data Ingestion

Reads all input CSVs from data/input/

Supports multiple channels and dates

🧼 2. Data Cleaning

Removes rows with missing product_id or invalid quantities

Filters out negative sales values

Handles missing numeric values safely

📊 3. Data Transformation

Derives revenue = quantity × price_per_unit

Extracts date from timestamp

Aggregates:

Total Sales & Revenue by Channel

Total Revenue per Day

Top 5 Products by Revenue

💾 4. Storage

Saves:

daily_channel_summary.csv

daily_revenue_summary.csv

top_5_products.csv

Inserts all results into sales_reports.db

🧠 5. Logging & Error Handling

Each step prints progress updates

Gracefully handles:

Missing files

Invalid data

Read/write issues

📈 Output Examples
Output File	Description
daily_channel_summary.csv	Total Sales & Revenue per Channel
daily_revenue_summary.csv	Total Daily Revenue
top_5_products.csv	Top 5 Products by Date
sales_reports.db	SQLite DB storing aggregated tables
🌐 Streamlit Dashboard Features

🎨 Animated background & modern UI

🧮 One-click data generation

🔁 Real-time transformation

📊 Beautiful interactive charts (via Plotly):

Bar Chart: Revenue by Channel

Facet Chart: Top 5 Products by Date

🚀 Future Enhancements

Automate pipeline scheduling via Airflow or AWS Lambda

Store raw/processed data in AWS S3 or Google Cloud Storage

Add Power BI or Tableau dashboards for advanced reporting

Integrate email/Slack alerts for daily summary

👨‍💻 Author

Channabasav Angadi
Data Engineer | Cloud & Data Engineer
📧 [channuangadi077@gmail.com]
🌐 [www.linkedin.com/in/channua](https://www.linkedin.com/in/channua/)