# @Author : Yulia
# @File   : clustering.py
# @Time   : 2025/9/3

import streamlit as st
import plotly.express as px
import pandas as pd


def render_clustering(filtered_data, render=True):
    # 检查 AI 数据是否存在
    if "Persona" not in filtered_data.columns:
        if render:
            st.warning("⚠️ AI Persona data missing. Please check data_loader.")
        return None, None

    # 1. 3D 散点图 (使用 AI 生成的 Persona 着色)
    # 对应简历: "visualizing AI-generated segments"
    fig_cluster = px.scatter_3d(
        filtered_data,
        x="Age",
        y="SessionsPerWeek",
        z="PlayerLevel",
        color="Persona",  # <--- 关键修改：展示 AI 标签
        hover_data=["Persona_Desc", "InGamePurchases"],
        title="🤖 AI-Driven Player Segmentation (5 Personas)",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    # 2. 统计各 Persona 的均值
    # 只取数值列进行平均
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