"""Data Preparation Script for Customer Segmentation Dashboard

This script prepares customer data for Power BI visualization by:
1. Connecting to the database
2. Executing segmentation queries
3. Processing and cleaning data
4. Exporting prepared datasets for Power BI
"""

import pandas as pd
import numpy as np
import pyodbc
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
DB_SERVER = os.getenv('DB_SERVER', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'customer_db')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')


def create_connection():
    """Create database connection"""
    try:
        connection_string = f"""
            DRIVER={{ODBC Driver 17 for SQL Server}};
            SERVER={DB_SERVER};
            DATABASE={DB_NAME};
            UID={DB_USER};
            PWD={DB_PASSWORD};
        """
        conn = pyodbc.connect(connection_string)
        print("Database connection successful")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def load_segmentation_query():
    """Load SQL query from file"""
    query_path = os.path.join('src', 'segmentation_query.sql')
    with open(query_path, 'r') as file:
        query = file.read()
    return query


def fetch_customer_data(conn):
    """Execute segmentation query and fetch results"""
    try:
        query = load_segmentation_query()
        df = pd.read_sql(query, conn)
        print(f"Fetched {len(df)} customer records")
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def clean_data(df):
    """Clean and preprocess customer data"""
    print("Cleaning data...")
    
    # Handle missing values
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Gender'].fillna('Unknown', inplace=True)
    df['Location'].fillna('Unknown', inplace=True)
    
    # Convert date columns to datetime
    date_columns = ['JoinDate', 'LastPurchaseDate', 'FirstPurchaseDate']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    # Remove duplicates
    df.drop_duplicates(subset=['CustomerID'], keep='first', inplace=True)
    
    # Handle outliers in monetary values (using IQR method)
    Q1 = df['Monetary'].quantile(0.25)
    Q3 = df['Monetary'].quantile(0.75)
    IQR = Q3 - Q1
    df['Monetary_Capped'] = df['Monetary'].clip(upper=Q3 + 1.5 * IQR)
    
    print(f"Data cleaned. Final record count: {len(df)}")
    return df


def add_derived_features(df):
    """Add additional features for analysis"""
    print("Adding derived features...")
    
    # Calculate customer tenure in months
    df['TenureMonths'] = ((datetime.now() - df['JoinDate']).dt.days / 30).astype(int)
    
    # Calculate days since last purchase
    df['DaysSinceLastPurchase'] = (datetime.now() - df['LastPurchaseDate']).dt.days
    
    # Calculate average days between purchases
    df['AvgDaysBetweenPurchases'] = df['CustomerLifetimeDays'] / df['Frequency'].replace(0, 1)
    
    # Create age groups
    df['AgeGroup'] = pd.cut(df['Age'], 
                            bins=[0, 25, 35, 45, 55, 65, 100],
                            labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+'])
    
    # Create revenue tiers
    df['RevenueTier'] = pd.cut(df['Monetary'],
                               bins=[0, 100, 500, 1000, 5000, float('inf')],
                               labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    # Calculate customer lifetime value (CLV) estimate
    df['EstimatedCLV'] = df['Monetary'] * (1 + df['PurchaseFrequencyRate'] * 365)
    
    print("Derived features added")
    return df


def export_to_csv(df, output_path='data/customer_segmentation_output.csv'):
    """Export prepared data to CSV for Power BI"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Data exported successfully to {output_path}")
    except Exception as e:
        print(f"Error exporting data: {e}")


def generate_summary_stats(df):
    """Generate summary statistics for validation"""
    print("\n=== Customer Segmentation Summary ===")
    print(f"Total Customers: {len(df)}")
    print(f"\nSegment Distribution:")
    print(df['CustomerSegment'].value_counts())
    print(f"\nAverage Metrics:")
    print(f"  - Average Recency: {df['Recency'].mean():.2f} days")
    print(f"  - Average Frequency: {df['Frequency'].mean():.2f} purchases")
    print(f"  - Average Monetary: ${df['Monetary'].mean():.2f}")
    print(f"\nActivity Status:")
    print(df['ActivityStatus'].value_counts())
    print("\n" + "="*40)


def main():
    """Main execution function"""
    print("Starting data preparation for Customer Segmentation Dashboard...\n")
    
    # Create database connection
    conn = create_connection()
    if conn is None:
        print("Failed to connect to database. Exiting.")
        return
    
    # Fetch customer data
    df = fetch_customer_data(conn)
    if df is None:
        print("Failed to fetch data. Exiting.")
        conn.close()
        return
    
    # Close database connection
    conn.close()
    
    # Clean and process data
    df = clean_data(df)
    df = add_derived_features(df)
    
    # Export processed data
    export_to_csv(df)
    
    # Generate summary statistics
    generate_summary_stats(df)
    
    print("\nData preparation completed successfully!")
    print("You can now import the output CSV into Power BI.")


if __name__ == "__main__":
    main()
