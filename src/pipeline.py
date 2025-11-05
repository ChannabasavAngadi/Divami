import pandas as pd
import os
import sqlite3
from glob import glob

def load_and_clean_data(input_folder):
    try:
        all_files = glob(os.path.join(input_folder, '*.csv'))
        if not all_files:
            print("No input files found.")
            return pd.DataFrame()

        df_list = []
        for file in all_files:
            print(f"Loading file: {file}")
            try:
                temp_df = pd.read_csv(file)
                df_list.append(temp_df)
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        df = pd.concat(df_list, ignore_index=True)
        print("Files successfully loaded and concatenated.")

        # Data Cleaning
        initial_count = len(df)
        df = df.dropna(subset=['product_id', 'quantity'])
        df = df[df['quantity'] > 0]
        cleaned_count = len(df)
        print(f"Cleaned data: removed {initial_count - cleaned_count} invalid rows.")
        
        return df

    except Exception as e:
        print(f"Error in load_and_clean_data: {e}")
        return pd.DataFrame()


def aggregate_data(df):
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['revenue'] = df['quantity'] * df['price_per_unit']
        
        # Revenue & sales by channel (per day)
        grouped = df.groupby(['date', 'channel']).agg(
            total_sales=('quantity', 'sum'),
            total_revenue=('revenue', 'sum')
        ).reset_index()
        print("Aggregated total sales and revenue by channel.")
        
        # Total revenue per day (all channels)
        daily_totals = df.groupby('date').agg(
            total_sales=('quantity', 'sum'),
            total_revenue=('revenue', 'sum')
        ).reset_index()
        print("Calculated total revenue per day.")
        
        return grouped, daily_totals
    except Exception as e:
        print(f"Error in aggregate_data: {e}")
        return pd.DataFrame(), pd.DataFrame()


def top_products(df):
    try:
        df['revenue'] = df['quantity'] * df['price_per_unit']
        top_products = (
            df.groupby(['date', 'product_id'])
              .agg(total_revenue=('revenue', 'sum'))
              .reset_index()
              .sort_values(['date', 'total_revenue'], ascending=[True, False])
        )
        print("Top products identified successfully.")
        return top_products.groupby('date').head(5)
    except Exception as e:
        print(f"Error in top_products: {e}")
        return pd.DataFrame()


def save_outputs(df_summary, df_top, df_daily, output_folder):
    try:
        os.makedirs(output_folder, exist_ok=True)

        summary_file = os.path.join(output_folder, 'daily_channel_summary.csv')
        top_file = os.path.join(output_folder, 'top_5_products.csv')
        daily_file = os.path.join(output_folder, 'daily_revenue_summary.csv')

        df_summary.to_csv(summary_file, index=False)
        df_top.to_csv(top_file, index=False)
        df_daily.to_csv(daily_file, index=False)

        print(f"Reports saved to {output_folder}")

        # Save to SQLite
        conn = sqlite3.connect('sales_reports.db')
        df_summary.to_sql('daily_summary', conn, if_exists='replace', index=False)
        df_top.to_sql('top_products', conn, if_exists='replace', index=False)
        df_daily.to_sql('daily_revenue', conn, if_exists='replace', index=False)
        conn.close()

        print("Data stored in SQLite database.")

    except Exception as e:
        print(f"Error in save_outputs: {e}")


# ✅ NEW FUNCTION to be imported in Streamlit
def process_sales_data():
    """Run the complete pipeline (for Streamlit or CLI)."""
    try:
        input_folder = os.path.join('data', 'input')
        output_folder = os.path.join('data', 'output')

        df = load_and_clean_data(input_folder)
        if df.empty:
            print("❌ No valid input data found.")
            return None

        summary, daily_totals = aggregate_data(df)
        top5 = top_products(df)
        save_outputs(summary, top5, daily_totals, output_folder)

        print("✅ Pipeline completed successfully.")
        return True

    except Exception as e:
        print(f"Error in process_sales_data: {e}")
        return False


if __name__ == "__main__":
    print("Starting sales data pipeline...")
    input_folder = os.path.join('data', 'input')
    output_folder = os.path.join('data', 'output')

    df = load_and_clean_data(input_folder)
    if not df.empty:
        summary, daily_totals = aggregate_data(df)
        top5 = top_products(df)
        save_outputs(summary, top5, daily_totals, output_folder)
        print("Pipeline completed successfully.")
    else:
        print("Pipeline stopped: No valid input data found.")