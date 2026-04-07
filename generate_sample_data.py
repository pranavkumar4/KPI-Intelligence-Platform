"""
Sample Data Generator
Creates realistic sample datasets for testing the KPI platform
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(rows=1000, filename='sample_data.csv'):
    """Generate sample business data"""
    
    np.random.seed(42)
    
    # Date range
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(rows)]
    
    # Generate sample data
    data = {
        'transaction_date': dates,
        'transaction_id': [f'TXN{str(i).zfill(6)}' for i in range(1, rows + 1)],
        'customer_id': [f'CUST{str(np.random.randint(1, 200)).zfill(4)}' for _ in range(rows)],
        'product_id': [f'PROD{str(np.random.randint(1, 50)).zfill(3)}' for _ in range(rows)],
        'region': np.random.choice(['North', 'South', 'East', 'West'], rows),
        'sales_channel': np.random.choice(['Online', 'Retail', 'Wholesale'], rows),
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Furniture', 'Books'], rows),
        'revenue': np.random.uniform(100, 5000, rows).round(2),
        'cost': np.random.uniform(50, 3000, rows).round(2),
        'quantity': np.random.randint(1, 100, rows),
        'discount_pct': np.random.uniform(0, 0.3, rows).round(3),
        'shipping_cost': np.random.uniform(5, 50, rows).round(2),
        'customer_satisfaction': np.random.uniform(1, 5, rows).round(1),
        'delivery_days': np.random.randint(1, 15, rows),
        'status': np.random.choice(['Completed', 'Pending', 'Cancelled', 'Returned'], rows, p=[0.7, 0.15, 0.1, 0.05]),
        'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'Cash', 'PayPal'], rows),
        'is_new_customer': np.random.choice([True, False], rows, p=[0.3, 0.7]),
        'website_visits': np.random.randint(1, 20, rows),
        'cart_abandonment_rate': np.random.uniform(0, 0.8, rows).round(3),
    }
    
    # Calculate profit
    df = pd.DataFrame(data)
    df['profit'] = df['revenue'] - df['cost'] - df['shipping_cost']
    df['profit_margin_pct'] = ((df['profit'] / df['revenue']) * 100).round(2)
    df['revenue_per_unit'] = (df['revenue'] / df['quantity']).round(2)
    
    # Add some missing values randomly
    for col in ['customer_satisfaction', 'delivery_days', 'website_visits']:
        mask = np.random.random(rows) < 0.1  # 10% missing
        df.loc[mask, col] = np.nan
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"✅ Sample data generated: {filename}")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"   Total revenue: ${df['revenue'].sum():,.2f}")
    print(f"   Total profit: ${df['profit'].sum():,.2f}")
    
    return df

if __name__ == "__main__":
    # Generate sample datasets of different sizes
    generate_sample_data(1000, 'sample_data_1k.csv')
    generate_sample_data(10000, 'sample_data_10k.csv')
    
    print("\n🎉 Sample data files created successfully!")
    print("   Use these files to test the KPI Intelligence Platform")
