# @Author : Yulia
# @File   : data_loader.py
# @Time   : 2025/9/6

import pandas as pd
import streamlit as st
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression

# 引入 AI 标签模块
import ai_persona


@st.cache_data
def load_data():
    """
    智能加载数据：优先读取清洗版，如果没有则读取原始版并自动清洗。
    同时执行 AI 计算流程。
    """

    # 1. 定义文件路径
    clean_file = "gaming_data_cleaned.csv"
    europe_file = "gaming_data_europe.csv"
    # 这里是你确认存在的原始 Kaggle 数据路径
    raw_file = "OnlineGamingBehavior/online_gaming_behavior_dataset.csv"

    # 2. 尝试加载数据
    if os.path.exists(clean_file):
        # 情况A：如果运行过 data_clean.py，直接读取清洗好的数据
        df = pd.read_csv(clean_file)
        # 尝试读取欧洲数据，如果没有就从 df 里切分
        if os.path.exists(europe_file):
            df_europe = pd.read_csv(europe_file)
        else:
            df_europe = df[df['Location'] == 'Europe'].copy()
    else:
        # 情况B：如果没有清洗好的文件，直接读取 Kaggle 原始数据
        # 这样保证你的 App 永远不会因为缺文件而报错
        try:
            df = pd.read_csv(raw_file)
            # 自动执行简单的清洗（去重）
            df = df.drop_duplicates()
            # 自动生成欧洲数据
            df_europe = df[df['Location'] == 'Europe'].copy()
        except FileNotFoundError:
            st.error(f" 错误：找不到原始数据文件。请确认 {raw_file} 存在。")
            return pd.DataFrame(), pd.DataFrame()

    # ================= AI PIPELINE START =================
    # 这一步是为了给数据加上 AI 标签 (Persona, Churn Risk)

    # --- A. AI Clustering (K-Means) ---
    # 选取特征
    clu_features = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    # 确保列存在，防止报错
    valid_clu_features = [c for c in clu_features if c in df.columns]

    if valid_clu_features:
        X_clu = df[valid_clu_features].fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_clu)

        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df["Cluster"] = kmeans.fit_predict(X_scaled)

        # 调用 LLM 模块打标签
        df = ai_persona.apply_persona_tags(df)
    else:
        # 如果列不对，给个默认值防止后续代码崩溃
        df["Persona"] = "Standard Player"

    # --- B. Predictive Analytics (Churn Risk) ---
    # 定义流失：每周会话少于 2 次
    if "SessionsPerWeek" in df.columns:
        df["Is_Churn"] = df["SessionsPerWeek"].apply(lambda x: 1 if x < 2 else 0)

        # 训练逻辑回归
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

    # 划分风险等级
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
    侧边栏筛选逻辑
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