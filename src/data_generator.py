import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_sales_data(channel, date_str, num_records):
    """Generates synthetic sales data for a specific channel and date."""
    start_time = datetime.strptime(date_str, '%Y-%m-%d')
    timestamps = [start_time + timedelta(minutes=np.random.randint(0, 24 * 60))
                  for _ in range(num_records)]

    product_ids = [f'P{i:04d}' for i in np.random.choice(range(10, 50), num_records)]
    quantities = np.random.randint(1, 15, num_records).astype(float)
    prices = np.round(np.random.uniform(50, 1000, num_records), 2)

    # Add some invalid data for cleaning demo
    if channel == 'web_app':
        product_ids[5] = None
        quantities[10] = -5
    if channel == 'physical_store':
        quantities[15] = np.nan

    data = pd.DataFrame({
        'timestamp': timestamps,
        'product_id': product_ids,
        'channel': channel,
        'quantity': quantities,
        'price_per_unit': prices
    })
    data['product_id'] = data['product_id'].astype(str)
    return data


def create_sample_files(target_date):
    """Creates sample input CSV files only for the specified date."""
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'input')
    os.makedirs(base_dir, exist_ok=True)

    print(f"--- Generating sample data for date: {target_date} ---")

    channels = {
        'web_app': 500,
        'mobile_app': 350,
        'physical_store': 150
    }

    all_data = []
    for channel, num_records in channels.items():
        date_formatted = target_date.replace('-', '')
        filename = f'{channel}_{date_formatted}.csv'
        filepath = os.path.join(base_dir, filename)

        df = generate_sales_data(channel, target_date, num_records)
        df.to_csv(filepath, index=False, float_format='%.2f')
        all_data.append(df)
        print(f"Created {filepath} with {len(df)} records.")

    final_df = pd.concat(all_data, ignore_index=True)
    print("\n✅ All files created successfully for the given date!")
    return final_df


if __name__ == '__main__':
    # Example test run (you can replace date)
    create_sample_files(target_date='2025-11-05')
