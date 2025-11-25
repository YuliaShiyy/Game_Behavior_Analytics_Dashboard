# @Author : Yulia
# @File   : clustering.py
# @Time   : 2025/9/3

import streamlit as st
import plotly.express as px
import pandas as pd


def render_clustering(filtered_data, render=True):
    # Check if AI data exists
    if "Persona" not in filtered_data.columns:
        if render:
            st.warning("⚠️ AI Persona data missing. Please check data_loader.")
        return None, None

    # 1. 3D scatter plot (using AI-generated Persona coloring)
    fig_cluster = px.scatter_3d(
        filtered_data,
        x="Age",
        y="SessionsPerWeek",
        z="PlayerLevel",
        color="Persona",  # <--- Key change: Display AI tag
        hover_data=["Persona_Desc", "InGamePurchases"],
        title="🤖 AI-Driven Player Segmentation (5 Personas)",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    # 2. Calculate the mean of each Persona.
    # Average only the numerical column
    numeric_cols = ["Age", "SessionsPerWeek", "PlayerLevel", "InGamePurchases"]
    cluster_summary = filtered_data.groupby("Persona")[numeric_cols].mean().round(2)

    if render:
        st.subheader("🧩 AI-Enhanced Player Segmentation")
        st.markdown("""
        > **AI Methodology:** Players are clustered into **5 distinct personas** using K-Means. 
        > Semantic tags (e.g., 'Whale', 'Grinder') were generated via **LLM Analysis** of behavioral patterns.
        """)

        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(fig_cluster, use_container_width=True)
        with col2:
            st.write("**Persona Distribution**")
            counts = filtered_data["Persona"].value_counts().reset_index()
            counts.columns = ["Persona", "Count"]
            fig_pie = px.pie(counts, values="Count", names="Persona", hole=0.4)
            fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.write("**📊 Behavioral Profile by Persona (Average Stats)**")
        st.dataframe(cluster_summary, use_container_width=True)


    return fig_cluster, cluster_summary
