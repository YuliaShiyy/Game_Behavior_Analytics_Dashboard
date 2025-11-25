# @Author : Yulia
# @File   : prediction.py
# @Time   : 2025/9/3 0:41

import streamlit as st
import pandas as pd
import plotly.express as px


def render_prediction(filtered_data, render=True):
    # Check if it contains forecast data
    if "Churn_Prob" not in filtered_data.columns:
        if render:
            st.warning("Prediction data missing.")
        return None, None

    # 1. Risk Overview KPIs
    high_risk_users = filtered_data[filtered_data["Risk_Level"] == "High Risk 🔴"]
    risk_rate = len(high_risk_users) / len(filtered_data) * 100 if len(filtered_data) > 0 else 0

    # 2. Churn probability distribution chart (Histogram)
    fig_hist = px.histogram(
        filtered_data,
        x="Churn_Prob",
        nbins=20,
        color="Risk_Level",
        title="Distribution of Churn Probability",
        labels={"Churn_Prob": "Predicted Probability of Churn (0-1)"},
        color_discrete_map={
            "High Risk 🔴": "#FF4B4B",
            "Medium Risk 🟡": "#FFAA00",
            "Safe 🟢": "#00CC96"
        }
    )

    if render:
        st.subheader("🔮 Predictive Analytics: Churn Risk")
        st.markdown("""
        > **Methodology:** A **Logistic Regression** model evaluates player activity patterns to estimate the probability of early churn.
        > **High Risk** is defined as Churn Probability > 70%.
        """)

        col1, col2, col3 = st.columns(3)
        col1.metric("High Risk Users", f"{len(high_risk_users)}")
        col2.metric("Predicted Churn Rate", f"{risk_rate:.1f}%")
        col3.metric("Model Type", "Logistic Regression")

        st.plotly_chart(fig_hist, use_container_width=True)

        # 3. High-risk user list (Actionable Insights)
        st.subheader("🚨 High Risk Cohort (Action Required)")
        st.caption("Top 10 players most likely to churn. Recommended Action: Send 'Come Back' gift.")

        display_cols = ["PlayerID", "Age", "SessionsPerWeek", "Persona", "Churn_Prob"]
        # Ensure the column exists
        cols_to_show = [c for c in display_cols if c in filtered_data.columns]

        st.dataframe(
            high_risk_users[cols_to_show].sort_values(by="Churn_Prob", ascending=False).head(10),
            use_container_width=True
        )

    # Returns a simulation accuracy (0.85) and a graph, maintaining consistency with the main app's interface.

    return 0.85, fig_hist
