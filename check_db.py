import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load hidden environment variables
load_dotenv()

print("🔍 Inspecting PostgreSQL Database...\n")

try:
    # 1. Connect to the database
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
    # 2. Query the table
    query = "SELECT transaction_id, amount, explanation, alert_time FROM fraud_alerts;"
    
    # 3. Load into a nice Pandas DataFrame for easy reading
    df = pd.read_sql_query(query, conn)
    
    if df.empty:
        print("📭 The database is currently empty.")
    else:
        print(f"✅ Found {len(df)} saved fraud alerts!")
        print("-" * 50)
        # Print the data beautifully
        pd.set_option('display.max_colwidth', None) # Don't truncate the explanation
        print(df)

except Exception as e:
    print(f"❌ Could not connect to database: {e}")
finally:
    if conn:
        conn.close()