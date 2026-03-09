🏦 Real-Time Bank Fraud Streaming Pipeline & GenAI Investigator
📌 Enterprise Overview
An end-to-end, event-driven machine learning microservice designed to process financial transactions in real-time. This pipeline decouples data ingestion from heavy ML compute, predicting fraud probabilities on the fly while handling severe class imbalances.

To bridge the gap between raw machine learning outputs and human fraud investigators, the system integrates Generative AI to automatically write natural-language context reports for any flagged transactions.

🏗️ System Architecture & Data Flow
Stream Ingestion (Apache Kafka): Simulated live credit card transactions are published continuously to a Kafka topic, decoupling the data source from the processing engine.

Stateful Feature Engineering (Redis): As transactions arrive, an in-memory Redis cache calculates stateful velocity features (e.g., time since the last transaction for this specific user) in milliseconds.

Inference Engine (FastAPI + XGBoost): A scalable FastAPI microservice consumes the Kafka stream and passes the enriched data to an optimized XGBoost classifier trained specifically on highly imbalanced anomaly data.

Explainable AI Layer (Google Gemini): If a transaction is flagged as fraudulent, the system triggers the Gemini API to dynamically generate a human-readable explanation of why the transaction looks suspicious based on the feature weights.

Observability & Storage (PostgreSQL + Streamlit): All transactions, predictions, and GenAI explanations are securely persisted in a PostgreSQL database and visualized in a live, auto-refreshing Streamlit dashboard.

💻 Tech Stack
Message Broker: Apache Kafka

In-Memory Cache: Redis

Backend API: FastAPI (Python)

Machine Learning: XGBoost, Pandas, Scikit-Learn

Generative AI: Google Gemini API

Database: PostgreSQL

Frontend/Dashboard: Streamlit

Containerization: Docker & Docker Compose

🚀 Key Engineering Features
Sub-Second Latency: Utilizes Redis as a high-speed feature store to prevent database bottlenecks during live model inference.

Imbalanced Classification: XGBoost model is strictly tuned using dynamic class-weighting (scale_pos_weight) to optimize for Recall and F1-Score rather than baseline accuracy.

Automated Investigation Reports: Replaces manual data auditing by using Gemini to translate tabular feature anomalies into plain English for security teams.

Full Containerization: The entire distributed system (Zookeeper, Kafka, Redis, Postgres, FastAPI, Streamlit) is orchestrated via Docker Compose for one-click deployment.