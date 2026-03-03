import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import time
import os
from dotenv import load_dotenv

# Load hidden environment variables
load_dotenv()

# 1. Configure the Page
st.set_page_config(page_title="Live Fraud Dashboard", page_icon="🚨", layout="wide")
st.title("🚨 Real-Time Bank Fraud Detection Dashboard")
st.markdown("Live streaming data from **Apache Kafka** → **FastAPI + XGBoost** → **PostgreSQL**")

# 2. Connect to PostgreSQL (Using SQLAlchemy to fix the pandas warning!)
@st.cache_resource
def init_connection():
    # Fetch credentials
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db_name = os.getenv("POSTGRES_DB")
    
    # Build the connection string securely
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(db_url)

engine = init_connection()

# 3. Create a placeholder to hold our live-updating UI
placeholder = st.empty()

# 4. The Live Auto-Refresh Loop
while True:
    try:
        # Fetch the latest data, ordered by newest first
        query = """
            SELECT transaction_id, amount, fraud_probability, explanation, alert_time 
            FROM fraud_alerts 
            ORDER BY alert_time DESC;
        """
        df = pd.read_sql(query, engine)
        
        # Inject the UI into the placeholder
        with placeholder.container():
            if df.empty:
                st.info("⏳ Waiting for live fraud alerts to stream in...")
            else:
                # Top Level Metrics
                total_alerts = len(df)
                latest_amount = df.iloc[0]['amount']
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Total Fraud Alerts", value=total_alerts)
                col2.metric(label="Latest Fraud Amount", value=f"${latest_amount:,.2f}")
                col3.metric(label="System Status", value="🟢 Live Stream Active")
                
                st.subheader("Recent Fraudulent Transactions & AI Explanations")
                
                # Display the data beautifully
                st.dataframe(
                    df.head(20).style.format({
                        "amount": "${:,.2f}", 
                        "fraud_probability": "{:.2%}" # Format as percentage
                    }), 
                    use_container_width=True,
                    hide_index=True
                )
                
    except Exception as e:
        st.error(f"Database connection error: {e}")
        
    # Wait 2 seconds before pulling new data
    time.sleep(2)