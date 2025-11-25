# @Author : Yulia
# @File   : data_loader.py
# @Time   : 2025/9/6

import pandas as pd
import streamlit as st
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression

import ai_persona


@st.cache_data
def load_data():
    """
    Intelligent data loading: Prioritizes reading the cleaned version; if unavailable, 
    reads the original version and automatically cleans it.

    Simultaneously executes AI computation processes.
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    
    # Define the path to the specific file
    clean_file = os.path.join(data_dir, "gaming_data_cleaned.csv")
    europe_file = os.path.join(data_dir, "gaming_data_europe.csv")

    raw_file = os.path.join(data_dir, "online_gaming_behavior_dataset.csv")

    # 2. Try loading data
    if os.path.exists(clean_file):
        # Scenario A: If data_clean.py has been run, directly read the cleaned data.
        df = pd.read_csv(clean_file)
        #Try reading European data; if not, split it from df.
        if os.path.exists(europe_file):
            df_europe = pd.read_csv(europe_file)
        else:
            df_europe = df[df['Location'] == 'Europe'].copy()
    else:
        # Scenario B: If there are no cleaned files, directly read the raw Kaggle data.
        # This ensures your app will never report an error due to missing files.
        try:
            df = pd.read_csv(raw_file)
            df = df.drop_duplicates()
            df_europe = df[df['Location'] == 'Europe'].copy()
        except FileNotFoundError:
            st.error(f" Error: Raw data file not found. Please verify that {raw_file} exists.")
            return pd.DataFrame(), pd.DataFrame()

    # ================= AI PIPELINE START =================
    # This step is to add AI labels (Persona, Churn Risk) to the data.

    # --- A. AI Clustering (K-Means) ---
    clu_features = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    # Ensure the column exists to prevent errors.
    valid_clu_features = [c for c in clu_features if c in df.columns]

    if valid_clu_features:
        X_clu = df[valid_clu_features].fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_clu)

        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df["Cluster"] = kmeans.fit_predict(X_scaled)

        # Tagging using the LLM module
        df = ai_persona.apply_persona_tags(df)
    else:
        # If the columns are incorrect, provide a default value to prevent subsequent code crashes.
        df["Persona"] = "Standard Player"

    # --- B. Predictive Analytics (Churn Risk) ---
    # Define churn as fewer than 2 sessions per week.
    if "SessionsPerWeek" in df.columns:
        df["Is_Churn"] = df["SessionsPerWeek"].apply(lambda x: 1 if x < 2 else 0)

        # Training Logistic Regression
        pred_features = ["Age", "PlayerLevel", "InGamePurchases"]
        valid_pred_features = [c for c in pred_features if c in df.columns]

        if valid_pred_features:
            X_pred = df[valid_pred_features].fillna(0)
            y_pred = df["Is_Churn"]

            model = LogisticRegression(max_iter=1000)
            try:
                model.fit(X_pred, y_pred)
                df["Churn_Prob"] = model.predict_proba(X_pred)[:, 1]
            except:
                df["Churn_Prob"] = 0.0
        else:
            df["Churn_Prob"] = 0.0
    else:
        df["Churn_Prob"] = 0.0

    # Risk level classification
    def risk_level(prob):
        if prob > 0.7:
            return "High Risk 🔴"
        elif prob > 0.4:
            return "Medium Risk 🟡"
        else:
            return "Safe 🟢"

    df["Risk_Level"] = df["Churn_Prob"].apply(risk_level)

    # ================= AI PIPELINE END =================

    return df, df_europe


def filter_data(df, selected_region, genres, genders, purchase_filter):
    """
    Sidebar Filtering Logic
    """
    data = df.copy()

    if selected_region != "Global":
        data = data[data["Location"] == selected_region]

    if genres:
        data = data[data["GameGenre"].isin(genres)]

    if genders:
        data = data[data["Gender"].isin(genders)]

    if purchase_filter == "Paid players":
        if "InGamePurchases" in data.columns:
            data = data[data["InGamePurchases"] == 1]
    elif purchase_filter == "Not-paid players":
        if "InGamePurchases" in data.columns:
            data = data[data["InGamePurchases"] == 0]


    return data
